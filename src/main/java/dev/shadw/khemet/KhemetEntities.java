package dev.shadw.khemet;

import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricEntityType;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.level.levelgen.Heightmap;

/** The creatures: the mummy and the royal mummy, each with a spawn egg and natural spawns in deserts. */
public final class KhemetEntities {
	public static final EntityType<Mummy> MUMMY = register("mummy", FabricEntityType.Builder.createMob(Mummy::new, MobCategory.MONSTER,
			b -> b.spawnRestriction(SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules)
					.defaultAttributes(Mummy::createAttributes)).sized(0.6F, 1.95F).clientTrackingRange(8));

	public static final EntityType<RoyalMummy> ROYAL_MUMMY = register("royal_mummy", FabricEntityType.Builder.createMob(RoyalMummy::new, MobCategory.MONSTER,
			b -> b.spawnRestriction(SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules)
					.defaultAttributes(RoyalMummy::createAttributes)).sized(0.6F, 1.95F).clientTrackingRange(8));

	public static final Item MUMMY_SPAWN_EGG = egg("mummy_spawn_egg", MUMMY);
	public static final Item ROYAL_MUMMY_SPAWN_EGG = egg("royal_mummy_spawn_egg", ROYAL_MUMMY);

	private KhemetEntities() {}

	private static <T extends net.minecraft.world.entity.Entity> EntityType<T> register(String path, EntityType.Builder<T> builder) {
		ResourceKey<EntityType<?>> key = ResourceKey.create(Registries.ENTITY_TYPE, ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, path));
		return Registry.register(BuiltInRegistries.ENTITY_TYPE, key, builder.build(key));
	}

	private static Item egg(String path, EntityType<? extends net.minecraft.world.entity.Mob> type) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, path));
		return Registry.register(BuiltInRegistries.ITEM, key, new SpawnEggItem(type, new Item.Properties().setId(key)));
	}

	/** Registers the entity types and their natural spawns. */
	public static void init() {
		BiomeModifications.addSpawn(BiomeSelectors.includeByKey(Biomes.DESERT), MobCategory.MONSTER, MUMMY, 12, 1, 3);
		BiomeModifications.addSpawn(BiomeSelectors.includeByKey(Biomes.DESERT), MobCategory.MONSTER, ROYAL_MUMMY, 1, 1, 1);
	}
}
