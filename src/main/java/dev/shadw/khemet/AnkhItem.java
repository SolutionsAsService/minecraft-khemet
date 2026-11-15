package dev.shadw.khemet;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** The Ankh of Life: use it to heal at once and then regenerate. It wears out and needs time between uses. */
public class AnkhItem extends LoreItem {
	public AnkhItem(Item.Properties properties, String loreKey) {
		super(properties, loreKey);
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		if (player.getHealth() >= player.getMaxHealth() && !player.hasEffect(MobEffects.POISON) && !player.hasEffect(MobEffects.WITHER)) {
			return InteractionResult.PASS;
		}
		if (!level.isClientSide) {
			player.heal((float) ContentData.d("ankh", "heal"));
			player.addEffect(new MobEffectInstance(MobEffects.REGENERATION, ContentData.i("ankh", "regen_seconds") * 20, ContentData.i("ankh", "regen_amplifier")));
			player.removeEffect(MobEffects.POISON);
			player.removeEffect(MobEffects.WITHER);
			stack.hurtAndBreak(1, player, hand == InteractionHand.MAIN_HAND ? EquipmentSlot.MAINHAND : EquipmentSlot.OFFHAND);
		}
		player.getCooldowns().addCooldown(stack, ContentData.i("ankh", "cooldown_ticks"));
		return InteractionResult.SUCCESS;
	}
}
