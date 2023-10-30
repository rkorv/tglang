#| /Type /XObject - describes an abstract XObject. See also
#| PDF::XObject::Form, PDF::XObject::Image
unit class PDF::XObject;

use PDF::COS::Stream;
use PDF::Class::Type;

also is PDF::COS::Stream;
also does PDF::Class::Type::Subtyped;

use PDF::COS::Tie;
use PDF::COS::Name;

has PDF::COS::Name $.Type is entry(:alias<type>) where 'XObject';
my subset XObjectSubtype of PDF::COS::Name where 'Form'|'Image'|'PS';
has XObjectSubtype $.Subtype is entry(:required, :alias<subtype>);

=begin pod

=comment adapted from [ISO-32000 Section 8.8 External Objects]

An external object (commonly called an C<XObject>) is a graphics object whose contents are defined by a self-
contained stream, separate from the content stream in which it is used. There are three types of external
objects:

=item An image XObject L<PDF::XObject::Image> represents a sampled visual image such as a photograph.
=item A form XObject L<PDF::Object::XObject::Form> is a self-contained description of an arbitrary sequence of
graphics objects.
=item A PostScript XObject L<PDF::Object::PS> contains a fragment of code expressed in the
PostScript page description language. PostScript XObjects should not be used.

=end pod
