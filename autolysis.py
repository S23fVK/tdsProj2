import os
import io
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai

def PYanalysis(data):
    return {"shape": data.shape, "columns": data.dtypes.to_dict(), "missing_values": data.isnull().sum().to_dict(), "summary_statistics": data.describe().to_dict()}

def LLManalysis(prompt):
    try:
        response = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "You are a data analysis assistant."},{"role": "user", "content": prompt}], max_tokens=500, temperature=0.7)
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error interacting with LLM: {e}")
        return None

def vis(data):
    numd = data.select_dtypes(include=['number'])
    if numd.empty:
        print("No numeric columns found for visualization.")
        return
    corr = numd.corr()
    plt.figure(figsize=(10, 9))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig("correlation_heatmap.png", bbox_inches='tight', pad_inches=0.2)
    plt.close()
    mis = data.isnull().sum()
    if mis.sum() > 0:
        mis = mis[mis > 0]
        plt.figure(figsize=(10, 9))
        sns.barplot(x=mis.index, y=mis.values, hue=mis.index, palette="viridis", legend=False)
        plt.title("Missing Values per Column")
        plt.xticks(rotation=30)
        plt.ylabel("Count")
        plt.xlabel("Column_name")
        plt.savefig("missing_values.png", bbox_inches='tight', pad_inches=0.2)
        plt.close()

def LLMstory(analysis, cfs):
    prompt = (
        f"The dataset has the following properties:\n"
        f"Shape: {analysis['shape']}\n"
        f"Columns: {analysis['columns']}\n"
        f"Missing Values: {analysis['missing_values']}\n"
        f"Summary Statistics: {analysis['summary_statistics']}\n"
        f"I have created the following visualizations: {', '.join(cfs)}.\n"
        "Please narrate a story summarizing the dataset, the analysis, and the key insights."
    )
    return LLManalysis(prompt)

token = os.environ.get("AIPROXY_TOKEN")
if not token:
    print("AIPROXY_TOKEN environment variable is not set. Use 'set AIPROXY_TOKEN=<token>' before running the program")
    sys.exit(1)
openai.api_key = token
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"

if len(sys.argv) != 2:
    print("Run program in this format - 'python autolysis.py <dataset.csv>'")
    sys.exit(1)
df = sys.argv[1]

with open(df, 'rb') as f:
    cont = f.read().decode('windows-1252', errors='ignore')
bfr = io.StringIO(cont)

try:
    data = pd.read_csv(bfr)
except Exception as e:
    print(f"Error loading dataset: {e}")
    sys.exit(1)

a = PYanalysis(data)
vis(data)
cf = ["correlation_heatmap.png"]
if data.isnull().sum().sum() > 0:
    cf.append("missing_values.png")
story = LLMstory(a, cf)
if story:
    with open("README.md", "w") as f:
        f.write("# Automated Data Analysis\n\n")
        f.write(story)
        f.write("\n\n## Visualizations\n")
        for c in cf:
            f.write(f"![{c}]({c})\n")
print("Analysis completed and results saved to README.md and PNG files successfully.")