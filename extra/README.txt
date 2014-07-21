El archivo bounding_boxes_persons.py fue el que utilice para hacer el etiquetado de las imagenes para el entrenamiento, usando el mismo formato que tenian los archivos de INRIA.

El archivo list_filenames_test_vers.py lo use para etiquetar las imagenes que utilice en los experimentos, los archivos que almacena tienen un formato mas sencillo.


El directorio person_detection tiene toas las imagenes resultantes y en ella se lleva a cabo el entrenamiento de los detectores. El script runall_script.sh manda a ejecutar uno a uno los entrenamientos.


En el directorio dataset vienen todas las imagenes que se usaron asi como sus respectivas etiquetas tanto para cabeza como para cabeza y hombros.


Si se ejecutan asi como se encuentran los scripts de python, deberian funcionar.

Antes de usar cualquier script de estos directorios se recomienda hacer un respaldo de todo ya que los scripts modifican muchas cosas y despues no se sabra si los reultados son los correctos ya que no existira un punto de comparacion.


---------------------------------------------------------------------------------------------------------------------------------

Todos los cuadros que se esten editando aparecen en verde, se pueden mover con el mouse si se hace click sobre ellos y se mantiene presionado. Una vez confirmados los cuadors estos cambian de color: azul es para cabezas y rojo es para cabezas y hombros.


Para usar los scripts:
		
	Flechas de navegacion:
		
		- derecha			Ver imagen siguiente.
		
		- izquierda		Ver imagen anterior.
		
		- arriba			Switch entre avanzar de una en una imagenes o de 10 en 10.
		

	Al presionar la tecla:	
		
		(EDICION)	
		
		- space		Agrega un cuadro para editar (cabeza y hombros).
		
		- alt			Agrega un cuadro para editar (cabezas).
		
		- a 			Se agrega un punto que marca el centro de lo que se quiere marcar ( hacer click con el mouse para verlo).
		
		- shift	 	(izquierdo) Reescala el cuadro a un tamaño mas pequeño.
		
		- ctrl  	(izquierdo) Confirma la posicion del objeto que se esta editando.
		
		- j				Hace que los cuadros del archivo se agreguen a la lista de los cuadros confirmados (cabezas).
		
		- k				Hace que los cuadros del archivo se agreguen a la lista de los cuadros confirmados (cabezas y hombros).
	
		- c				Se eliminan los cuadros rojos (cabezas y hombros).
		
		- x				Elimina el ultimo cuadro confirmado, los escritos en el archivo no se eliminan (cabeza y hombros).
		
		- s				Elimina el ultimo cuadro confirmado, los escritos en el archivo no se eliminan (cabezas).
		
		- z				Elimina el ultimo punto confirmado, los escritos en el archivo no se eliminan.
			
		(GENERALES)
		
		- u				Se cortan, escalan y almacenan las todas las imagenes etiquetadas en los directorios señalados.
		
		- q				Se eliminan los cuadro de toda la imagen (si no se guardan los cambios, esto no afecta el archivo donde se almacenan los cuadros).
		
		- enter		Confirmacion de todo lo editado por imagen, todos los cuadros y puntos confirmados se escriben en el archivo.
			
			
			
			
			
			
			
			
			
			
			
			
	
