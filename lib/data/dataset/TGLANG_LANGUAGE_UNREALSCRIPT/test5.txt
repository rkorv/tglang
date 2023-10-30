//=============================================================================
// Copyright 2005-2012 Eliot Van Uytfanghe. All Rights Reserved.
// GameInfo.bPlayersMustBeReady is recommended for this game.
// Do not enable Translocators.
//=============================================================================
class BTServer_BunnyMode extends BTServer_TrialMode;

static function bool DetectMode( MutBestTimes M )
{
    return CTFGame(M.Level.Game) != none;
}

protected function InitializeMode()
{
    super.InitializeMode();
    bSoloMap = true;
    MRI.bSoloMap = true;

    CTFGame(Level.Game).bDefaultTranslocator = false;
}

function ModeModifyPlayer( Pawn other, Controller c, BTClient_ClientReplication CRI )
{
    super.ModeModifyPlayer( other, c, CRI );

    if( CRI.bPermitBoosting )
    {
        CRI.ProhibitedCappingPawn = Other;
    }
}

function bool ChatCommandExecuted( PlayerController sender, string command, string value )
{
    local bool bmissed;
    local BTClient_ClientReplication CRI;

    switch( command )
    {
        case "boost":
            CRI = GetRep( sender );
            if( CRI != none )
            {
                CRI.bPermitBoosting = !CRI.bPermitBoosting;
                if( CRI.bPermitBoosting )
                {
                    CRI.ProhibitedCappingPawn = sender.Pawn;
                }
                sender.ClientMessage( "Boosting on:" @ CRI.bPermitBoosting );
            }
            break;

        default:
            bmissed = true;
            break;
    }

    if( !bmissed )
        return true;

    return super.ChatCommandExecuted( sender, command, value );
}

defaultproperties
{
    ModeName="BT"
    ModePrefix="CTF"
    ConfigClass=class'BTServer_BunnyModeConfig'

    ExperienceBonus=5
}
