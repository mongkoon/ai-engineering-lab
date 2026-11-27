# Publishing the sanitized project to GitHub

Repository target:

`cloud/aws/sagemaker/breast-cancer-pipeline/`

The distribution ZIP is rooted at the same repository-relative directory. After extracting it **at the root of a local clone** of the repository, the files land in the intended folder.

```bash
git clone https://github.com/mongkoon/ai-engineering-lab.git
cd ai-engineering-lab
unzip /path/to/breast-cancer-pipeline-github-ready-verified.zip
# Inspect the changed file list before staging
git status --short
# Add only the intended project folder
git add cloud/aws/sagemaker/breast-cancer-pipeline
# Carefully inspect staged content and any filenames
git diff --cached --stat
git diff --cached --check
git commit -m "Document SageMaker breast cancer pipeline experiments"
git push origin main
```

**The ZIP itself is not a repository file.** Extract it locally before committing. Existing placeholder `.gitkeep` files may remain; they are harmless but optional to remove once real files exist.

## Public-data review

Before publishing, check for:

- Account IDs, exact role ARNs, access keys or other credentials
- Personal identifiers, local machine paths or private file names
- Original execution notebooks or screenshots containing account details
- New `.env` files, ZIP backups, models or endpoints

This bundle excludes private execution outputs and original full-screen images. Curated notebooks have no execution outputs. The archival notebooks render sanitized original cell source as non-executable Markdown. The exact AWS account and personal identifiers can be kept in a separate private archive, not committed to the public repository.
