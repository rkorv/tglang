#| /Type /Annot Annotations
unit class PDF::Annot;

use PDF::Class::StructItem;
use PDF::Class::Type;

also is PDF::COS::Dict;
also does PDF::Class::StructItem;
also does PDF::Class::Type;

use PDF::COS::Tie;
use PDF::COS::Tie::Array;
use PDF::COS::Name;
use PDF::COS::DateString;
use PDF::COS::TextString;
use PDF::Appearance;
use PDF::Border;
use PDF::OCG;   # optional content group
use PDF::OCMD;  # optional content membership dict
my subset OCG-or-OCMD where PDF::OCG|PDF::OCMD;
use PDF::Page;

use ISO_32000::Table_164-Entries_common_to_all_annotation_dictionaries;
also does ISO_32000::Table_164-Entries_common_to_all_annotation_dictionaries;

method cb-init {
    use PDF::Field :coerce-field, :FieldLike;
    # annots are also sometimes fields
    coerce-field(self, PDF::Field)
        if self ~~ FieldLike && self !~~ PDF::Field;
}

has PDF::COS::Name $.FT is entry(:inherit, :alias<field-type>);   # Include this, just to help discover if we're a field

# See [PDF Spec 1.7 table 8.15 - Entries common to all annotation dictionaries ]
has PDF::COS::Name $.Type is entry(:alias<type>) where 'Annot';
use PDF::Class::Defs :AnnotSubtype;
has PDF::COS::Name $.Subtype is entry(:required, :alias<subtype>) where AnnotSubtype;
has Numeric @.Rect is entry(:required, :len(4), :alias<rect>);    # (Required) The annotation rectangle, defining the location of the annotation on the page in default user space units.
has PDF::COS::TextString $.Contents is entry(:alias<content>);    # (Optional) Text to be displayed for the annotation or, if this type of annotation does not display text, an alternate description of the annotation’s contents in human-readable form
has PDF::Page $.P is entry(:alias<page>);                         # (Optional; PDF 1.3; not used in FDF files) An indirect reference to the page object with which this annotation is associated.
has PDF::COS::TextString $.NM is entry(:alias<annotation-name>);  # (Optional; PDF 1.4) The annotation name, a text string uniquely identifying it among all the annotations on its page.
my subset ModTime where PDF::COS::DateString | PDF::COS::TextString;
sub coerce-mod-time(Str $s is rw, ModTime) {
    my $class := $s ~~ PDF::COS::DateString::DateRegex
        ?? PDF::COS::DateString
        !! PDF::COS::TextString;
    $s = $class.COERCE($s);
}
has ModTime $.M is entry(:coerce(&coerce-mod-time), :alias<mod-time>);                # (Optional; PDF 1.1) The date and time when the annotation was most recently modified.
# The preferred format is a date string, but viewer applications should be prepared to accept and display a string in any format.
# See [ISO-32000 Table 165 - Annotation flags]
my Int enum AnnotFlag is export(:AnnotFlag) « :AnnotInvisable(1) :AnnotHidden(2) :AnnotPrint(3) :AnnotNoZoom(4) :AnnotNoRotate(5) :AnnotNoView(6) :AnnotReadOnly(7) :AnnotLocked(8) :AnnotToggleNoView(9) :AnnotLockedContents(10) »;
my subset AnnotFlagsInt of UInt where ^(2 +< 10);
has AnnotFlagsInt $.F is entry(:alias<annot-flags>, :default(0));              # (Optional; PDF 1.1) A set of flags specifying various characteristics of the annotation
has PDF::Appearance $.AP is entry(:alias<appearance>);      # (Optional; PDF 1.2) An appearance dictionary specifying how the annotation is presented visually on the page
has PDF::COS::Name $.AS is entry(:alias<appearance-state>); # (Required if the appearance dictionary AP contains one or more subdictionaries; PDF 1.2) The annotation’s appearance state, which selects the applicable appearance stream from an appearance subdictionary
role Border does PDF::COS::Tie::Array {
    has Numeric $.horizontal-radius is index(0, :required);
    has Numeric $.vertical-radius is index(1, :required);
    has Numeric $.width is index(2, :required);
    has Numeric @.dash-pattern is index(3, :array-or-item);
}
has Border $.Border is entry(:default[0, 0, 1]);            # (Optional) An array specifying the characteristics of the annotation’s border. The border is specified as a rounded rectangle.
has Numeric @.C is entry(:alias<color>);                    # (Optional; PDF 1.1) An array of numbers in the range 0.0 to 1.0, representing a color used for (*) background, when closed, (*) title bar of pop-up window, (*) link border
has UInt $.StructParent is entry(:alias<struct-parent>);                           # (Required if the annotation is a structural content item; PDF 1.3) The integer key of the annotation’s entry in the structural parent tree
has OCG-or-OCMD $.OC is entry(:alias<optional-content>);    # (Optional; PDF 1.5) An optional content group or optional content membership dictionary specifying the optional content properties for the annotation.

has Hash $.DR is entry(:alias<default-resources>);          # In PDF 1.2, an additional entry in the field dictionary, DR, was defined but was never implemented. Beginning with PDF 1.5, this entry is obsolete and should be ignored.

method annots {
    my @ = self;
}
