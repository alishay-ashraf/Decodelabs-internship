(defun c:Setup3DProject ()
  ;; 1. Configure Workspace Layers & Color Hierarchy
  (command "-layer" "m" "Object" "c" "Red" "" "l" "Continuous" "" "")     ; Primary 3D solid geometry [cite: 34, 35, 36]
  (command "-layer" "m" "Border" "c" "Green" "" "l" "Continuous" "" "")   ; Drawing sheets & title blocks [cite: 34, 37]
  (command "-layer" "m" "Dim"    "c" "Blue" "" "l" "Continuous" "" "")    ; Parametric dimensions [cite: 34, 38]
  (command "-layer" "m" "Viewports" "c" "Cyan" "" "l" "Continuous" "" "") ; Multi-view layout frames [cite: 34, 39]
  
  ;; Set the active layer to Object for 3D modeling
  (setvar "CLAYER" "Object")
  
  ;; 2. Disable 'Save UCS with viewport' to prevent coordinate misalignment
  (setvar "UCSVP" 0) ; [cite: 69]
  
  ;; 3. Set the spatial navigation workspace to Southeast Isometric
  (command "VPOINT" "1,-1,1") ; 
  (princ "\nWorkspace configured! [cite: 33] Layer structure established  and Viewport UCS protection active[cite: 69].")
  
  ;; 4. Volumetric Transformation Framework (Input -> Process)
  (princ "\n--- STEP 1: INPUT ---")
  (princ "\nDraw a PERFECTLY CLOSED flat boundary line/polyline now (e.g., CIRCLE or PLINE) [cite: 74, 75, 83].")
  (command "POLYLINE") ; Invokes input line sequence [cite: 74]
  
  (princ "\n--- STEP 2: PROCESS ---")
  (princ "\nOnce your closed sketch is ready, convert it to a REGION to ensure a solid volume[cite: 85, 86]:")
  (princ "\nCommand hint: REGION -> Select your object [cite: 74, 86]")
  (princ "\nCommand hint: EXTRUDE -> Select region -> Enter extrusion height [cite: 14, 76]")
  
  ;; 5. Constructive Solid Geometry Demonstration Reminder (Boolean algebraic logic)
  (princ "\n--- STEP 3: BOOLEAN LOGIC ---")
  (princ "\nTo combine or subtract features on your gear/bracket, use[cite: 9, 13, 15]:")
  (princ "\n- UNION (Fuses solid volumes together) [cite: 9, 14, 76]")
  (princ "\n- SUBTRACT (Cuts a core/hole out of a solid component) [cite: 9, 14, 76]")
  
  (princ "\n\nSetup Complete! Proceed with building your solid 3D geometry[cite: 13].")
  (princ)
)