from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from chains import generate_chain, reflect_chain

REFLECT = "reflect"
GENERATE = "generate"


class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_graph(max_messages: int = 8):
    """
    Builds and compiles the generate <-> reflect graph.

    max_messages controls how many reflection rounds happen before the
    graph stops. Each round adds 2 messages (one generation + one
    reflection), so max_messages=8 gives ~3 rounds of back-and-forth.
    """

    def generation_node(state: MessageGraph):
        return {"messages": [generate_chain.invoke({"messages": state["messages"]})]}

    def reflection_node(state: MessageGraph):
        res = reflect_chain.invoke({"messages": state["messages"]})
        return {"messages": [HumanMessage(content=res.content)]}

    def should_continue(state: MessageGraph):
        if len(state["messages"]) > max_messages:
            return END
        return REFLECT

    builder = StateGraph(state_schema=MessageGraph)
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)
    builder.set_entry_point(GENERATE)
    builder.add_conditional_edges(
        GENERATE,
        should_continue,
        {
            REFLECT: REFLECT,
            END: END,
        },
    )
    builder.add_edge(REFLECT, GENERATE)

    return builder.compile()