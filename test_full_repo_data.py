import asyncio
from app.core.github_client import GitHubClient

async def main():
    client = GitHubClient()
    data = await client.get_full_repo_data('https://github.com/tiangolo/fastapi')
    print('full_name:', data['metadata']['full_name'])
    print('readme length:', len(data['readme']))

if __name__ == '__main__':
    asyncio.run(main())
