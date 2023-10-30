function read_nfgs_specfit, galaxy, _extra=extra
; jm04mar15uofa
    
    specfitpath = nfgs_path(/specfit)
    root = 'nfgs_int'

    specfit = irdspecfit(galaxy,specfitpath=specfitpath,root=root,$
      objtagname='GALAXY',_extra=extra)
    
return, specfit
end
