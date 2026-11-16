package dev.shadw.khemet;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.blockrenderlayer.v1.BlockRenderLayerMap;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.minecraft.client.renderer.RenderType;
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
		// plants have transparent pixels: without a cutout layer they render with a black background
		BlockRenderLayerMap.INSTANCE.putBlocks(RenderType.cutout(), KhemetBlocks.BLUE_LOTUS, KhemetBlocks.PAPYRUS);
		dev.shadw.khemet.mobs.GeneratedMobsClient.initClient();
	}
}
