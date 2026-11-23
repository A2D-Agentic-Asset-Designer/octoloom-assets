<span class="ol-pill">Connect and secure</span>

# LLM authentication

<p class="lede"><strong>How a broker authenticates to its LLM: an API key or OAuth 2.0 (JWT).</strong> Keys stay out of the files: they are secret variables asked at deploy time.</p>

!!! info "Where to find it"
    LLM card → **Authentication**

<figure markdown>
![The LLM in the broker inspector](../assets/ui/network-v1-exchange-llm-light.webp#only-light){ loading=lazy }
![The LLM in the broker inspector](../assets/ui/network-v1-exchange-llm-dark.webp#only-dark){ loading=lazy }
<figcaption>The LLM in the broker inspector</figcaption>
</figure>

## How to use it

1. Select the LLM card and choose **API key** or **OAuth 2.0**.
2. Enter the variable names; the values are asked at deploy time.

## In detail

By default an LLM connection uses an **API key** and the gateway adds its transcoding policy. For an LLM behind your own gateway that expects a **JWT**, choose *OAuth 2.0 client credentials* on the connection: the egress gateway fetches the token from your identity provider, caches it and sends `Authorization: Bearer <token>` with every LLM call.

- **Fill in for…** writes the authentication block and the `exchange.json` variables for Microsoft Entra ID, Okta, Auth0, Keycloak, Salesforce, Amazon Cognito, PingOne, Anypoint connected apps or any other provider. **Show steps** lists the setup at the provider.
- The LLM must declare an **Input format** (`openai`, `anthropic` or `gemini`) and the kind under *Supported authentication*, otherwise the CLI only accepts an API key (build error 3060). Octoloom flags this in Problems and adds both before a build when the platform is clear. API key setups are not changed.



## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### LLM provider

<div class="grid" markdown>

![card-llm](../assets/ui/card-llm-light.webp#only-light){ loading=lazy }
![card-llm](../assets/ui/card-llm-dark.webp#only-dark){ loading=lazy }

The model provider and models brokers may use. The key comes from a connection secret at deploy time. A dashed icon tile means the LLM is referenced from Exchange (an exchange.json dependency, classifier llm-metadata), not declared in this project; its Platform and Models are read-only on the card.

**When to use it:** Every network that has a 1.0 broker or AgentScript LLM nodes.

</div>

**Examples and details:**

- OpenAI gpt-5-mini
- Azure OpenAI deployment
- Dashed tile: MuleSoft openai from Exchange, shared by every project that references it

### Connection

Where and how the gateway reaches an agent, MCP server or LLM: URL, authentication and policies.

**When to use it:** One per upstream. Change URLs per environment with variables.

**Examples and details:**

- ${refundAgent.url} with PII detection inbound
- openai_connection with apiKey ${openai.apiKey}
- MCP connection URL = server base without /mcp; Test connection calls exactly what the runtime calls
