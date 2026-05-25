import asyncio
from app.core.github_client import GitHubClient

async def main():
    client = GitHubClient()
    data = await client._get('https://api.github.com/repos/tiangolo/fastapi')
    print('full_name:', data.get('full_name'))

if __name__ == '__main__':
    asyncio.run(main())
