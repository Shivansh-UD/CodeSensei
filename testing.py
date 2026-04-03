from mcpServer.githubServer import listFiles, getFile

# Test 1 — list all code files in your own repo
print("=== FILES ===")
files = listFiles("https://github.com/Shivansh-UD/CodeSensei")
for f in files:
    print(f)

# Test 2 — read githubServer.py since that's the only file with content
print("\n=== FILE CONTENT ===")
code = getFile("https://github.com/Shivansh-UD/CodeSensei", "mcpServer/githubServer.py")
print(code)