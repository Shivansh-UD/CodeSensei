import requests
import base64
from mcp.server.fastmcp import FastMCP
from config import GITHUB_TOKEN

mcp = FastMCP("codesensei")

# List of file extensions we care about. We use this to get all the code files only
CODE_EXTENSIONS = [
    ".py", ".js", ".ts", ".java", ".cpp", ".c",
    ".go", ".rs", ".rb", ".php", ".cs", ".swift"
]


"""
Headers are required for every GitHub API request we make.

Authorization → proves to GitHub who we are using our token.
                without this we are anonymous and limited to
                only 60 requests per hour which runs out fast.
                with it we get 5000 requests per hour.

Accept        → tells GitHub to send the response in its latest
                and most reliable JSON format. without it GitHub
                still works but may use an older format.
"""

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def parseUrl(repoUrl: str):
    urlSplit =repoUrl.split("/")
    owner = urlSplit[3]
    repo = urlSplit[4]
    return owner, repo

@mcp.tool()
def listFiles(repoUrl: str) -> list[str]:
    owner1, repo1 = parseUrl(repoUrl)
    url = f"https://api.github.com/repos/{owner1}/{repo1}/git/trees/HEAD?recursive=1"
    response = requests.get(url, headers=headers)
    data = response.json()  # converts response to Python dictionary
    files = [] # empty list to push the code files in
    for i in data["tree"]: # data is in dictionary form so firstly we have to loop starting with data["tree"]. THIS IS THE FIRST KEY WE HAVE TO GET INSIDE AND LOOP.
        if i["type"] == "blob" and any(i["path"].endswith(ext) for ext in CODE_EXTENSIONS): # THIS IS THE SECOND KEY WE HAVE TO GET INSIDE AND LOOP AND HERE WE LOOK FOR THE FILES ENDING WITH STUFF IN CODE_EXTENSIONS LIST
            files.append(i["path"])
    return files


@mcp.tool()  
def getFile(repoUrl: str, filePath: str) -> str:
    owner2, repo2 = parseUrl(repoUrl)
    #This is how we make custom URL in Python
    url = f"https://api.github.com/repos/{owner2}/{repo2}/contents/{filePath}"  #filePath is basically like the end of the file paths where it usualy goes like /blob/main/agent1.py or similar stuff
    response = requests.get(url, headers=headers)
    data = response.json()
    encoded_content = data["content"]
    decoded_bytes = base64.b64decode(encoded_content)
    raw_code = decoded_bytes.decode("utf-8")
    return raw_code

if __name__ == "__main__":
    mcp.run()