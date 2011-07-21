
(define (script-fu-batch-scale-ratio globexp ratio)
  (define (resize-img n f)
   (let* ((fname (car f))
          (img (car (gimp-file-load 1 fname fname))))
       (let* (
             (drawable   (car (gimp-image-active-drawable img)))
             (cur-width  (car (gimp-image-width img)))
             (cur-height (car (gimp-image-height img)))
          (new-width  (* ratio cur-width))
          (new-height (* ratio cur-height))
             (new_ratio      (min (/ new-width cur-width) (/ new-height cur-height)))
             (width      (* new_ratio cur-width))
             (height     (* new_ratio cur-height))
          )
    
         (gimp-image-undo-disable img)
         (gimp-image-scale img width height)
         (gimp-file-save 1 img (car (gimp-image-get-active-drawable img)) fname fname)
         (gimp-image-delete img)
      )
    )
    (if (= n 1) 1 (resize-img (- n 1) (cdr f)))
  )
  (let* ((files (file-glob globexp 0)))
     (resize-img (car files) (car (cdr files))))
)

(script-fu-register "script-fu-batch-scale-ratio"
          _"Batch Image Scale By Ratio"
          "Hey!"
          "Nicholas Herring and Richard Hirner (http://www.gimptalk.com/forum/topic/Script-fu-Batch-Resi-e-9440-1.html) & ADP (http://www.adp-gmbh.ch/misc/tools/script_fu/ex_10.html), hello_earth"
          "2008, Nicholas Herring based on a script by Richard Hirner"
          "March 26, 2008"
          ""
          SF-STRING "Full path with wildcards" "C:\\Test\\*.jpg"
          SF-VALUE "Scaling ratio (min 0.01, max 1)" "0.50")
(script-fu-menu-register "script-fu-batch-scale-ratio"
          "<Toolbox>/Xtns/Jobhunt/Misc")
