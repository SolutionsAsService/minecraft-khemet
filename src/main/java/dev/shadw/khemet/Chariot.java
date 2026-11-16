package dev.shadw.khemet;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * A war chariot: a craftable vehicle for two. Use it to climb aboard (the first rider drives, the second rides); the driver steers with the look
 * direction, forward to go, back to brake, sprint for a burst. It climbs one block, takes no fall damage and, when it is broken, drops the chariot
 * item. The two horses in its model are drawn, not alive: the chariot is the engine. The model is generated from mobs/chariot.json.
 */
public class Chariot extends Mob {
	public Chariot(EntityType<? extends Chariot> type, Level level) {
		super(type, level);
		setPersistenceRequired();
	}

	public static AttributeSupplier.Builder createAttributes() {
		return Mob.createMobAttributes()
				.add(Attributes.MAX_HEALTH, 40.0)
				.add(Attributes.MOVEMENT_SPEED, 0.32)
				.add(Attributes.STEP_HEIGHT, 1.0)
				.add(Attributes.KNOCKBACK_RESISTANCE, 0.6);
	}

	@Override
	public boolean removeWhenFarAway(double distance) {
		return false;
	}

	@Override
	public boolean canBeLeashed() {
		return false;
	}

	@Override
	public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
		return false;
	}

	@Override
	protected boolean canAddPassenger(Entity passenger) {
		return getPassengers().size() < 2;
	}

	@Override
	public LivingEntity getControllingPassenger() {
		return getFirstPassenger() instanceof Player player ? player : null;
	}

	@Override
	protected InteractionResult mobInteract(Player player, InteractionHand hand) {
		if (player.isSecondaryUseActive()) {
			return InteractionResult.PASS;
		}
		if (!level().isClientSide && getPassengers().size() < 2) {
			player.startRiding(this);
		}
		return InteractionResult.SUCCESS;
	}

	@Override
	protected void tickRidden(Player player, Vec3 input) {
		super.tickRidden(player, input);
		setRot(player.getYRot(), player.getXRot() * 0.5F);
		yRotO = yBodyRot = yHeadRot = getYRot();
	}

	@Override
	protected Vec3 getRiddenInput(Player player, Vec3 input) {
		return new Vec3(0.0, 0.0, player.zza >= 0.0F ? player.zza : player.zza * 0.3F);
	}

	@Override
	protected float getRiddenSpeed(Player player) {
		return (float) getAttributeValue(Attributes.MOVEMENT_SPEED) * (player.isSprinting() ? 1.3F : 1.0F);
	}
}
