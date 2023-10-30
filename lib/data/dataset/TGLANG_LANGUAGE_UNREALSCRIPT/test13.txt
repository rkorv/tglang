//-----------------------------------------------------------
// used to draw the inpoints of the Camerapath
//-----------------------------------------------------------
class RotKnoten extends Engine.Actor;

var float dct;
var float a[100];
var float b[100];
var float c[100];
var int i;
var int n;
var vector v;

function PostBeginPlay()
{
}

defaultproperties
{
     Texture=Texture'Engine_res.SunIcon'
     DrawScale=0.500000
}
