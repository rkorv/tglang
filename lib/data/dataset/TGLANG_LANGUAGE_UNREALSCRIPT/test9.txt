/**
 * Copyright 1998-2011 Epic Games, Inc. All Rights Reserved.
 */
class CullDistanceVolume extends Volume
	native
	hidecategories(Advanced,Attachment,Collision,Volume)
	placeable;

/**
 * Helper structure containing size and cull distance pair.
 */
struct native CullDistanceSizePair
{
	/** Size to associate with cull distance. */
	var() float Size;
	/** Cull distance associated with size. */
	var() float CullDistance;
};

/**
 * Array of size and cull distance pairs. The code will calculate the sphere diameter of a primitive's BB and look for a best
 * fit in this array to determine which cull distance to use.
 */
var() array<CullDistanceSizePair> CullDistances;

/**
 * Whether the volume is currently enabled or not.
 */
var() bool bEnabled;

// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)
// (cpptext)

cpptext
{
	/**
	 * Called after change has occured - used to force update of affected primitives.
	 */
	virtual void PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent);

	/**
	 * bFinished is FALSE while the actor is being continually moved, and becomes TRUE on the last call.
	 * This can be used to defer computationally intensive calculations to the final PostEditMove call of
	 * eg a drag operation.
	 */
	virtual void PostEditMove(UBOOL bFinished);

	/**
	 * Returns whether the passed in primitive can be affected by cull distance volumes.
	 *
	 * @param	PrimitiveComponent	Component to test
	 * @return	TRUE if tested component can be affected, FALSE otherwise
	 */
	static UBOOL CanBeAffectedByVolumes( UPrimitiveComponent* PrimitiveComponent );

	/**
	 * Get the set of primitives and new max draw distances defined by this volume.
	 */
	void GetPrimitiveMaxDrawDistances(TMap<UPrimitiveComponent*,FLOAT>& OutCullDistances);

}


defaultproperties
{
   CullDistances(1)=(Size=10000.000000)
   bEnabled=True
   Begin Object Class=BrushComponent Name=BrushComponent0 Archetype=BrushComponent'Engine.Default__Volume:BrushComponent0'
      ReplacementPrimitive=None
      bAcceptsLights=True
      bDisableAllRigidBody=True
      AlwaysLoadOnClient=True
      AlwaysLoadOnServer=True
      LightingChannels=(bInitialized=True,Dynamic=True)
      Name="BrushComponent0"
      ObjectArchetype=BrushComponent'Engine.Default__Volume:BrushComponent0'
   End Object
   BrushComponent=BrushComponent0
   Components(0)=BrushComponent0
   CollisionType=COLLIDE_CustomDefault
   bCollideActors=False
   CollisionComponent=BrushComponent0
   Name="Default__CullDistanceVolume"
   ObjectArchetype=Volume'Engine.Default__Volume'
}
