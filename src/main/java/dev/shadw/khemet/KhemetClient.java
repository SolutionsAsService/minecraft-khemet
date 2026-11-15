package dev.shadw.khemet;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.ZombieRenderer;
import net.minecraft.client.renderer.entity.state.ZombieRenderState;
import net.minecraft.resources.ResourceLocation;

/** Client side: the mummies reuse the zombie model with their own skins. */
public class KhemetClient implements ClientModInitializer {
	private static ResourceLocation texture(String name) {
		return ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, "textures/entity/" + name + ".png");
	}

	/** A zombie-shaped creature with its own skin. */
	static class SkinnedZombieRenderer extends ZombieRenderer {
		private final ResourceLocation skin;

		SkinnedZombieRenderer(EntityRendererProvider.Context context, ResourceLocation skin) {
			super(context);
			this.skin = skin;
		}

		@Override
		public ResourceLocation getTextureLocation(ZombieRenderState state) {
			return skin;
		}
	}

	@Override
	public void onInitializeClient() {
		EntityRendererRegistry.register(KhemetEntities.MUMMY, ctx -> new SkinnedZombieRenderer(ctx, texture("mummy")));
		EntityRendererRegistry.register(KhemetEntities.ROYAL_MUMMY, ctx -> new SkinnedZombieRenderer(ctx, texture("royal_mummy")));
	}
}
