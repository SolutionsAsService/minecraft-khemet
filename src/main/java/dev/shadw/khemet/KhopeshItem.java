package dev.shadw.khemet;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.EntityTypeTags;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/** Anubis's Khopesh: a curved sword that cuts the undead for extra damage. */
public class KhopeshItem extends LoreItem {
	public KhopeshItem(Item.Properties properties, String loreKey) {
		super(properties, loreKey);
	}

	@Override
	public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
		if (target.getType().is(EntityTypeTags.UNDEAD) && target.level() instanceof ServerLevel server) {
			target.hurtServer(server, attacker.damageSources().magic(), (float) ContentData.d("khopesh", "undead_bonus"));
		}
		return super.hurtEnemy(stack, target, attacker);
	}
}
