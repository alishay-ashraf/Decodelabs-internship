import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

MASTER_TEMPLATE = """
You are an expert growth marketer and copywriter.

Generate a high-converting, engaging piece of marketing copy for the product specified below.

Product Name: {product_name}
Target Tone: {tone}
Platform: {platform}

Strict structural constraints for this platform:
{platform_constraints}

Write the copy now:
"""


def compile_prompt(product_name: str, platform: str, tone: str) -> str:
    platform_lower = platform.lower()

    if "linkedin" in platform_lower:
        constraints = (
            "- Include 2-3 relevant hashtags at the bottom.\n"
            "- Use professional formatting suitable for B2B readers."
        )
    elif "instagram" in platform_lower:
        constraints = (
            "- Start with a strong visual hook.\n"
            "- Limit to 3 short paragraphs max and use emojis naturally.\n"
            "- End with a clear CTA."
        )
    elif "email" in platform_lower:
        constraints = (
            "- Provide a subject line at the top.\n"
            "- Structure with introduction, bullet points, and sign-off."
        )
    elif "twitter" in platform_lower or "x" in platform_lower:
        constraints = (
            "- Entire output must be under 280 characters.\n"
            "- No headers or filler text."
        )
    else:
        constraints = "- Adapt appropriately for the platform."

    return MASTER_TEMPLATE.format(
        product_name=product_name,
        tone=tone,
        platform=platform,
        platform_constraints=constraints
    )


async def generate_copy(
    client: httpx.AsyncClient,
    product_name: str,
    platform: str,
    tone: str,
    temperature: float
):
    compiled_prompt = compile_prompt(product_name, platform, tone)

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": compiled_prompt}
        ],
        "temperature": temperature,
        "max_tokens": 300
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30.0
        )

        if response.status_code != 200:
            return {
                "product": product_name,
                "status": "Failed",
                "error": response.text
            }

        data = response.json()

        return {
            "product": product_name,
            "platform": platform,
            "tone": tone,
            "status": "Success",
            "copy": data["choices"][0]["message"]["content"].strip()
        }

    except Exception as e:
        return {
            "product": product_name,
            "status": "Failed",
            "error": str(e)
        }


async def main():
    batch_jobs = [
        {"product": "EcoStride Sneakers", "platform": "Instagram", "tone": "Witty", "temp": 0.8},
        {"product": "Quantum SaaS Analytics", "platform": "LinkedIn", "tone": "Professional", "temp": 0.2},
        {"product": "HydroFlask Pro", "platform": "Twitter/X", "tone": "Bold & Punchy", "temp": 0.7},
        {"product": "Fintech Budget App Launch", "platform": "Email", "tone": "Factual & Informative", "temp": 0.2},
    ]

    async with httpx.AsyncClient() as client:
        tasks = [
            generate_copy(
                client,
                job["product"],
                job["platform"],
                job["tone"],
                job["temp"]
            )
            for job in batch_jobs
        ]

        results = await asyncio.gather(*tasks)

        print("\n--- Results ---\n")

        for res in results:
            if res["status"] == "Success":
                print(f"✅ {res['product']}")
                print(res["copy"])
                print("-" * 60)
            else:
                print(f"❌ {res['product']}")
                print("Error:", res["error"])
                print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())