format IMP_GeographicLiving BEST12.0;
label IMP_GeographicLiving = 'Imputed GeographicLiving';
IMP_GeographicLiving = GeographicLiving;
if GeographicLiving = . then IMP_GeographicLiving = 4;
