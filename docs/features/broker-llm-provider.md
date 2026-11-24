<span class="ol-pill">Connect and secure</span>

# LLM provider

<p class="lede"><strong>The language model a broker uses: OpenAI, Azure OpenAI, Gemini, an A²D LLM mock or an LLM published in Exchange.</strong> The LLM decides cost and quality; an A²D LLM mock lets you deploy and chat without an LLM key.</p>

!!! info "Where to find it"
    Broker card → **LLM** · Asset Palette → **LLMs**

<figure markdown>
![A 1.0 broker with an LLM from Exchange](../assets/ui/network-v1-exchange-llm-light.webp#only-light){ loading=lazy }
![A 1.0 broker with an LLM from Exchange](../assets/ui/network-v1-exchange-llm-dark.webp#only-dark){ loading=lazy }
<figcaption>A 1.0 broker with an LLM from Exchange</figcaption>
</figure>

## How to use it

1. Select the broker and pick its **LLM** in the inspector, or drag an LLM from the Asset Palette.

2. Set the model and its URL variable.

    <figure markdown>
    ![A²D LLM mocks in the palette](../assets/ui/assets-a2d-llm-light.webp#only-light){ loading=lazy }
    ![A²D LLM mocks in the palette](../assets/ui/assets-a2d-llm-dark.webp#only-dark){ loading=lazy }
    <figcaption>A²D LLM mocks in the palette</figcaption>
    </figure>

3. Save, build and deploy.

## In detail

Select a broker and choose its LLM provider and model in the inspector:

- **v1**: writes `spec.llm` (provider reference, connection, model).
- **v2**: writes the `llm` block and `config.default_llm` of the broker's `.agent` file.
- A v2 broker's **Kind** and **Implementation** are in a *Protected broker settings* section with a lock, like the protected part of `exchange.json`: read-only until you unlock it.

An LLM whose URL points to a MuleSoft / Flex gateway is labelled **via Omni gateway**. Variables are resolved from the `exchange.json` defaults; secrets are never shown.

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
