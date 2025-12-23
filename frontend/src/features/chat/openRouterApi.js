import { http } from "@/shared/api/http";

export async function openRouterRequest({ text, apiKey }) {
    const res = await http("/OpenRouter/request/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            text,
            api_key: apiKey,
        }),
    });

    return res.json();
}