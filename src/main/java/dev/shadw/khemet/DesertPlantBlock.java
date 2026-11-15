package dev.shadw.khemet;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.state.BlockState;

/** A river-and-oasis plant (blue lotus, papyrus): it grows on sand and dirt, which ordinary flowers refuse. */
public class DesertPlantBlock extends FlowerBlock {
	public DesertPlantBlock(Holder<MobEffect> effect, float seconds, Properties properties) {
		super(effect, seconds, properties);
	}

	@Override
	protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
		return state.is(BlockTags.SAND) || state.is(BlockTags.DIRT) || state.is(net.minecraft.world.level.block.Blocks.CLAY)
				|| state.is(net.minecraft.world.level.block.Blocks.SANDSTONE);
	}
}
