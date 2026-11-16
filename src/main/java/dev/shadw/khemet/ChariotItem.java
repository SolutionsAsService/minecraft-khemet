package dev.shadw.khemet;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.context.UseOnContext;

/** Sets a chariot down on the block you use it on. */
public class ChariotItem extends Item {
	public ChariotItem(Properties properties) {
		super(properties);
	}

	@Override
	public InteractionResult useOn(UseOnContext context) {
		if (!(context.getLevel() instanceof ServerLevel level)) {
			return InteractionResult.SUCCESS;
		}
		BlockPos pos = context.getClickedPos().relative(context.getClickedFace());
		Chariot chariot = KhemetVehicles.CHARIOT.spawn(level, context.getItemInHand(), context.getPlayer(), pos, EntitySpawnReason.SPAWN_ITEM_USE, true, false);
		if (chariot == null) {
			return InteractionResult.FAIL;
		}
		chariot.setYRot(context.getRotation());
		context.getItemInHand().consume(1, context.getPlayer());
		return InteractionResult.SUCCESS_SERVER;
	}
}
