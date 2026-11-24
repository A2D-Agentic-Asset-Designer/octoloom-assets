<span class="ol-pill">Before you start · 3 of 6</span>

# Connected app Octoloom-CA

Octoloom acts as a **connected app** (client credentials), with only the scopes it needs.

1. In Anypoint, click the **settings** gear → **Access Management**, then **Connected Apps** → **Create app**.

   ![The settings menu with Access Management](../assets/onboarding/ca-access-mgmt.png)


   ![Access Management side bar with Connected Apps](../assets/onboarding/ca-nav.png)


   ![Connected Apps, Owned Apps, Create app](../assets/onboarding/ca-create.png)

2. **Name**: `Octoloom-CA`. **Type**: *App acts on its own behalf (client credentials)*.

   ![Create App: the name and App acts on its own behalf (client credentials)](../assets/onboarding/ca-name.png)


   ![Scopes: Add Scopes](../assets/onboarding/ca-scopes.png)

3. **Add Scopes**, for your business group and the environment(s) you deploy to:

   | Area | Scope | Used for |
   |---|---|---|
   | General | View Organization, View Environment | business groups and environments |
   | Exchange | Exchange Viewer | the Asset Palette, governance rulesets |
   | Exchange | Exchange Contributor | Publish |
   | Runtime Manager | Read Applications, Create Applications | Deploy and the status lights |
   | Gateways | read access to the Omni Gateways | the gateway chips of the Deploy form |
   | API Manager | View APIs Configuration, Manage APIs Configuration, Manage Policies | broker instances and their policies |
   | Monitoring | Monitoring Viewer | Traces and the Tracer (optional) |

   Use **Filter scopes** to find each one; don't tick whole groups.

   ![The Add Scopes list with a filter box](../assets/onboarding/ca-scope-list.png)

   Then pick your **business group** and the **environments** (for example Sandbox), and review.

   ![Select Business Groups](../assets/onboarding/ca-groups.png)


   ![Select Environments: Sandbox and Design](../assets/onboarding/ca-envs.png)


   ![Review: every scope with its business group and environments](../assets/onboarding/ca-review.png)

4. **Add Scopes**, then **Save**, and copy the **Client ID** and **Client Secret**.

   ![Save the connected app](../assets/onboarding/ca-save.png)


Least privilege: add only these. If a call is refused (HTTP 403), Octoloom names the permission that is missing; add just that one. Don't *Select all*.

Keep the secret out of files and chats: Octoloom stores it in the VS Code secret storage.


---

**Next:** [Connect Octoloom to Agent Fabric](connect-anypoint.md)
