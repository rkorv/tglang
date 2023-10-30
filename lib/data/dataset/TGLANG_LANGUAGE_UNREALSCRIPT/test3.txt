// Zombie Monster for KF Invasion gametype
class ZEDS_ZombieClot extends ZombieClot_STANDARD
    Config(ApocZEDPack);

struct SZEDInfo {
	var config int ForcedMinPlayers;
	var config int Health;
    var config int HeadHealth;
    var config float PlayerCountHealthScale;
    var config float PlayerNumHeadHealthScale;
};
var config SZEDInfo ZEDInfo;

simulated function PostBeginPlay()
{
    if (ZEDInfo.Health>0 && Health!=ZEDInfo.Health)
    {
        Health = ZEDInfo.Health;
        HealthMax = ZEDInfo.Health;
    }

    if (ZEDInfo.HeadHealth>0 && HeadHealth!=ZEDInfo.HeadHealth)
        HeadHealth = ZEDInfo.HeadHealth;

    if (ZEDInfo.PlayerCountHealthScale>0 && PlayerCountHealthScale!=ZEDInfo.PlayerCountHealthScale)
        PlayerCountHealthScale = ZEDInfo.PlayerCountHealthScale;

    if (ZEDInfo.PlayerNumHeadHealthScale>0 && PlayerNumHeadHealthScale!=ZEDInfo.PlayerNumHeadHealthScale)
        PlayerNumHeadHealthScale = ZEDInfo.PlayerNumHeadHealthScale;
		
	Super.PostBeginPlay();
}

function float NumPlayersHealthModifer()
{
    if (ZEDInfo.ForcedMinPlayers>0)
        return 1.0 + (ZEDInfo.ForcedMinPlayers - 1) * PlayerCountHealthScale;
    return Super.NumPlayersHealthModifer();
}

function float NumPlayersHeadHealthModifer()
{
    if (ZEDInfo.ForcedMinPlayers>0)
        return 1.0 + (ZEDInfo.ForcedMinPlayers - 1) * PlayerNumHeadHealthScale;
    return Super.NumPlayersHeadHealthModifer();
}

defaultproperties
{
    DrawScale=1.1
    Prepivot=(Z=5.0)
    bUseExtendedCollision=true
    ColOffset=(Z=48)
    ColRadius=25
    ColHeight=5
    damageForce=5000
    ScoringValue=7
    SoundRadius=80
    SoundVolume=50
    CollisionRadius=26.000000
    RotationRate=(Yaw=45000,Roll=0)
    GroundSpeed=105.000000
    WaterSpeed=105.000000
    MeleeDamage=6
    JumpZ=340.000000
    MeleeRange=20.0//30.000000
    bCannibal = true
    MenuName="Clot"
    Intelligence=BRAINS_Mammal
    GrappleDuration=1.5
    SeveredHeadAttachScale=0.8
    SeveredLegAttachScale=0.8
    SeveredArmAttachScale=0.8
    ClotGrabMessageDelay=12.0
    HeadHeight=2.0
    HeadScale=1.1
    CrispUpThreshhold=9
    OnlineHeadshotOffset=(X=20,Y=0,Z=37)
    OnlineHeadshotScale=1.3
    MotionDetectorThreat=0.34
    Health=130//200
    HealthMax=130//200
    HeadHealth=25
    PlayerCountHealthScale=0.6 //0.25 kyan
    PlayerNumHeadHealthScale=0.15 //0.0 kyan
}
