***** License ******************************************************************
* Optimal Design of Mixed AC-DC Distribution Systems For Commercial Buildings: *
* A Nonconvex Generalized Benders Decomposition Approach                       *
*                                                                              *
* Copyright (C) 2014  Stephen M. Frank (stephen.frank@ieee.org)                *
*                                                                              *
* This program is free software: you can redistribute it and/or modify         *
* it under the terms of the GNU General Public License as published by         *
* the Free Software Foundation, either version 3 of the License, or            *
* (at your option) any later version.                                          *
*                                                                              *
* This program is distributed in the hope that it will be useful,              *
* but WITHOUT ANY WARRANTY; without even the implied warranty of               *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                *
* GNU General Public License for more details.                                 *
*                                                                              *
* You should have received a copy of the GNU General Public License            *
* along with this program.  If not, see <http://www.gnu.org/licenses/>.        *
********************************************************************************

$TITLE Test Script: AC-DC Model
$ONTEXT

    Filename : test-model.gms
    Author   : Stephen Frank
    Release  : March 1, 2014
    Version  : 1.1

    Provides a compilation test for the AC-DC model and performs GAMSCHK
    diagnostics on the compiled model. Valid data is required.

    Compile-time control settings:
        DataFile                Name of the input data file
        RelPath                 Relative path to AC-DC model files
        Reform (yes/no)         Use the reformulation of the model?
        ConvexRelaxation        Specify one of:
                                linear = McCormick inequalities + valid cuts
                                quadratic = Convex quadratic underestimator,
                                    linear overestimator
                                piecewise = Piecewise linear
                                none/no/[Anything else] = Does nothing
        PiecewiseType           For bilinear terms; specify one of:
                                mccormick = Uses McCormick inequalities
                                logtransform = Uses a log transformation
        NumSeg                  Number of segments for linear and piecewise
                                linear relaxations
                                
    To execute the test:
        1. Set an appropriate file name in %DataFile%
        2. Ensure that %DataFile% is in the current working directory
        3. Set the remaining compile-time control settings as appropriate for
           the version of the model you wish to test.
        4. Adjust GAMSCHK control parameters as desired by modifying the output
           to be written to 'test-model.gck'
        5. Run the script
        6. Ensure there are no compilation errors
        7. Examine the listing for GAMSCHK output

    NOTES:
    1. If you are working with the reformulated model, your data file must
       include big M values as computed using the script 'AC-DC-big-M.gms'. The
       output from 'test-big-M.gms' satisfies this requirement.
    2. For the reformulated model, if no relaxation type is specified then the
       script compiles the exact reformulation. If a relaxation type is
       specified, then the script compiles the relaxation. By default, the
       script is configured to test the linear relaxation of the model.
    3. The compile-time setting %PiecewiseType% has no effect unless
       %ConvexRelaxation%==piecewise.
    4. If GAMSCHK is configured to output the full list of equations, it is
       recommended to use a low value for the number of segments %NumSeg%
       employed for linear or piecewise linear relaxations. Otherwise, the
       equation listing becomes very large.

$OFFTEXT

** Enable C and C++ style comments
* End-of-line
$EOLCOM //
$ONEOLCOM

* In-line
$INLINECOM /* */
$ONINLINE

* * * MODIFY SETTINGS HERE  * * * * * * * * * * * * * * * * * * * * * * * * * *

** Test Controls
* GDX file to import from
$SET DataFile threebus_big_M

* Relative path to AC-DC files
$SET RelPath ../Formulation

* Use reformulation?
$SET Reform yes

* Use a convex relaxation? (Valid for reformulation only)
*   Choose one of: linear, quadratic, piecewise
*   If 'piecewise', also choose piecewise type: mccormick, logtransform
$SET ConvexRelaxation linear
$SET PiecewiseType mccormick

* Number of segments to use in linear and piecewise linear relaxations:
$SET NumSeg 2

** Create GAMSCHK control file
* Writes the GAMSCHK control file 
$ONECHO > test-model.gck
DISPLAYCR
    Equations
    # Add a list below, or leave blank to get them all

BLOCKLIST

BLOCKPIC

PICTURE
$OFFECHO

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


* =============================================================================
*  Perform Test
* =============================================================================
** Required Flags
* What to load?
$SET LoadSets               yes
$SET LoadParams             yes
$SET LoadVars               no
$SET InitVars               yes
$SET LoadBigM               %Reform%

* Display zero rows/columns for equations/vars
option LIMROW = 0;
option LIMCOL = 0;


** Include Files
* Disable listing of includes (doesn't seem to work?)
$OFFINCLUDE

* Default compile time settings
$INCLUDE %RelPath%/AC-DC-defaults.gms

* Set, Parameter, and Variable Definitions
$INCLUDE %RelPath%/AC-DC-defs.gms

* Set & Data Processing
$INCLUDE %RelPath%/AC-DC-data.gms

* Equations
$IFTHEN %Reform% == no
$INCLUDE %RelPath%/AC-DC-equations-original.gms
$ELSE
$INCLUDE %RelPath%/AC-DC-equations-reform.gms
$IFTHEN.relax NOT %ConvexRelaxation% == none
$INCLUDE %RelPath%/AC-DC-equations-relax.gms
$ENDIF.relax
$ENDIF


** Define Model
* Create the model
model ACDCtest /all/ ;

** Check Model
* Set solver to GAMSCHK (used to examine model properties)
option MINLP = GAMSCHK;

* Run checks
solve ACDCtest using MINLP minimizing z;
