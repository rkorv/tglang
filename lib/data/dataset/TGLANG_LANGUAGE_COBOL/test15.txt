*> These are equivalent.
INVOKE my-class "foo" RETURNING var
MOVE my-class::"foo" TO var *> Inline method invocation
