package dev.shadw.khemet;

import net.fabricmc.fabric.api.object.builder.v1.entity.FabricEntityType;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.item.Item;
import net.minecraft.world.phys.Vec3;

/** The craftable vehicles: the war chariot and its item. */
public final class KhemetVehicles {
	public static final EntityType<Chariot> CHARIOT = register("chariot", FabricEntityType.Builder.createMob(Chariot::new, MobCategory.MISC, b -> b.defaultAttributes(Chariot::createAttributes))
			.sized(2.0F, 1.4F).passengerAttachments(new Vec3(0.0, 0.55, 0.35), new Vec3(0.0, 0.55, -0.45)).clientTrackingRange(10));

	public static final Item CHARIOT_ITEM = item("chariot");

	private KhemetVehicles() {}

	private static <T extends net.minecraft.world.entity.Entity> EntityType<T> register(String path, EntityType.Builder<T> builder) {
		ResourceKey<EntityType<?>> key = ResourceKey.create(Registries.ENTITY_TYPE, ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, path));
		return Registry.register(BuiltInRegistries.ENTITY_TYPE, key, builder.build(key));
	}

	private static Item item(String path) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, path));
		return Registry.register(BuiltInRegistries.ITEM, key, new ChariotItem(new Item.Properties().setId(key).stacksTo(1)));
	}

	/** Touching this class registers the vehicle and its item. */
	public static void init() {}
}
