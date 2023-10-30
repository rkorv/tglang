select
    address,
    name_tag as tag,
    label as label
from {{ source('ethereum', 'tags_raw') }}
