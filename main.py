import argparse
from core.graph.graph import build_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-xml", type=str, help="Path to XML file", required=True)
    parser.add_argument("--input-bug-list", type=str, help="Path to bugs CSV file", required=True)
    parser.add_argument("--output", type=str, help="Where to store the output report", default="reports")
    parser.add_argument("--format", type=str, choices=['html', 'markdown'], default='html', help="Output format type")

    args = parser.parse_args()

    input_state = {
        "xml_path": args.input_xml,
        "csv_path": args.input_bug_list
    }

    compiled_graph = build_graph()
    result = compiled_graph.invoke(input_state)
    output = result.get("output")

    print(output)

if __name__ == "__main__":
    main()
