package dev.shadw.khemet;

import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.component.ItemAttributeModifiers;

/** The first artifact (the Ankh of Life) and weapon (Anubis's Khopesh). The potion ingredients come from potions.json. */
public final class KhemetItems {
	public static final Item ANKH = item("ankh", p -> new AnkhItem(
			p.durability(ContentData.i("ankh", "durability")).rarity(Rarity.RARE).fireResistant(), "item.khemet.ankh.lore"));

	public static final Item KHOPESH = item("khopesh", p -> new KhopeshItem(
			p.durability(ContentData.i("khopesh", "durability")).rarity(Rarity.RARE).enchantable(14).attributes(ItemAttributeModifiers.builder()
					.add(Attributes.ATTACK_DAMAGE, new AttributeModifier(Item.BASE_ATTACK_DAMAGE_ID, ContentData.d("khopesh", "damage"),
							AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)
					.add(Attributes.ATTACK_SPEED, new AttributeModifier(Item.BASE_ATTACK_SPEED_ID, ContentData.d("khopesh", "attack_speed_modifier"),
							AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND)
					.build()), "item.khemet.khopesh.lore"));

	private KhemetItems() {}

	private static Item item(String path, Function<Item.Properties, Item> factory) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath(Mod.MOD_ID, path));
		return Registry.register(BuiltInRegistries.ITEM, key, factory.apply(new Item.Properties().setId(key)));
	}

	/** Touching this class registers the items. */
	public static void init() {}
}
