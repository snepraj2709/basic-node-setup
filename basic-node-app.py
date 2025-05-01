import os
import subprocess
import json
import sys

def run(cmd, cwd=None):
    print(f"➡️  Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def create_project(project_name):
    if os.path.exists(project_name):
        print(f"❌ Folder '{project_name}' already exists.")
        return

    os.makedirs(f"{project_name}/src", exist_ok=True)
    os.chdir(project_name)

    # Step 1: Init + install dependencies
    run("npm init -y")
    run("npm install typescript ts-node @types/node --save-dev")
    run("npm install express")
    run("npm install --save-dev @types/express")
    run("npm install --save-dev nodemon")

    # Step 2: Initialize and overwrite tsconfig.json
    run("npx tsc --init")
    print("🛠️  Overwriting tsconfig.json with custom settings...")
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "CommonJS",
            "rootDir": "src",
            "outDir": "dist",
            "esModuleInterop": True,
            "strict": True,
            "skipLibCheck": True
        }
    }
    with open("tsconfig.json", "w") as f:
        json.dump(tsconfig, f, indent=2)

    # Step 3: ESLint + Prettier setup
    run("npm install eslint prettier eslint-config-prettier eslint-plugin-prettier --save-dev")

    print("🛠️  Creating ESLint config...")
    eslint_config = {
        "env": {
            "browser": True,
            "es2021": True,
            "node": True
        },
        "extends": [
            "eslint:recommended",
            "plugin:prettier/recommended"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaVersion": "latest",
            "sourceType": "module"
        },
        "plugins": ["prettier"],
        "rules": {
            "prettier/prettier": "error"
        }
    }
    with open(".eslintrc.json", "w") as f:
        json.dump(eslint_config, f, indent=2)

    with open(".prettierrc", "w") as f:
        f.write(json.dumps({
            "semi": True,
            "singleQuote": True,
            "printWidth": 80,
            "tabWidth": 2,
            "trailingComma": "es5"
        }, indent=2))

    print("📝 Creating src/index.ts with Express code...")
    express_code = '''/** @format */

import express, { Request, Response } from 'express';
const app = express();
const port = 3000;

app.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
'''
    with open("src/index.ts", "w") as f:
        f.write(express_code)

    print("🔧 Updating package.json scripts...")
    with open("package.json", "r") as f:
        pkg = json.load(f)

    pkg["scripts"] = {
        "dev": "nodemon --watch src --exec ts-node src/index.ts",
        "build": "tsc",
        "start": "node dist/index.js",
        "lint": "eslint . --ext .ts",
        "format": "prettier --write ."
    }

    with open("package.json", "w") as f:
        json.dump(pkg, f, indent=2)

    print(f"\n✅ Project '{project_name}' is ready!")
    print("➡️  To get started:")
    print(f"   cd {project_name}")
    print("   npm install")
    print("   npm run build")
    print("   npm run dev")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_node_ts_project.py <project-name>")
    else:
        create_project(sys.argv[1])
        print("Project created successfully!")
        print("Done!")

        # Start the server automatically
        project_path = os.path.abspath(sys.argv[1])
        os.chdir(project_path)
        run("npm install")
        run("npm run build")
        run("npm run dev")
        print("Server started successfully!")