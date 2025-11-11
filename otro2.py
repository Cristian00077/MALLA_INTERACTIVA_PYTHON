import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Malla Interactiva UNINORTE")
        self.root.geometry("500x350")
        self.root.configure(bg='#e8e8e8')
        
        # Centrar la ventana
        self.centrar_ventana(500, 350)
        
        # Título
        titulo = tk.Label(
            self.root,
            text="Bienvenid@ a la malla interactiva de UNINORTE",
            font=('Arial', 14, 'bold'),
            bg='#e8e8e8',
            fg='#333333'
        )
        titulo.pack(pady=30)
        
        # Label para selección
        label_carrera = tk.Label(
            self.root,
            text="Seleccione la carrera:",
            font=('Arial', 14),
            bg='#e8e8e8',
            fg='#333333'
        )
        label_carrera.pack(pady=10)
        
        # ComboBox para seleccionar carrera
        self.carreras = [
            "Seleccione",
            "Ingenieria de sistemas",
            "Ingenieria Civil",
            "Ingenieria Mecánica",
            "Ingenieria Electrica",
            "Ingenieria Electronica",
            "Ingenieria Industrial"
        ]
        
        self.combo_carrera = ttk.Combobox(
            self.root,
            values=self.carreras,
            state='readonly',
            font=('Arial', 11),
            width=25
        )
        self.combo_carrera.current(0)
        self.combo_carrera.pack(pady=10)
        
        # Botón Aceptar
        btn_aceptar = tk.Button(
            self.root,
            text="Aceptar",
            font=('Arial', 11),
            bg='#f0f0f0',
            fg='#333333',
            padx=40,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            command=self.abrir_malla
        )
        btn_aceptar.pack(pady=15)
        
        # Botón Salir
        btn_salir = tk.Button(
            self.root,
            text="Salir",
            font=('Arial', 11),
            bg='#f0f0f0',
            fg='#333333',
            padx=40,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            command=self.root.quit
        )
        btn_salir.pack(pady=5)
    
    def centrar_ventana(self, ancho, alto):
        """Centra la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - ancho) // 2
        y = (screen_height - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def abrir_malla(self):
        """Abre la ventana de la malla curricular según la carrera seleccionada"""
        carrera_seleccionada = self.combo_carrera.get()
        
        if carrera_seleccionada == "Seleccione":
            messagebox.showwarning(
                "Advertencia",
                "Por favor seleccione una carrera"
            )
            return
        
        # Mapeo de nombres de carreras a nombres de archivos JSON
        mapeo_archivos = {
            "Ingenieria de sistemas": "Sistemas.json",
            "Ingenieria Civil": "Civil.json",
            "Ingenieria Mecánica": "Mecanica.json",
            "Ingenieria Electrica": "Electrica.json",
            "Ingenieria Electronica": "Electronica.json",
            "Ingenieria Industrial": "Industrial.json"
        }
        
        nombre_archivo = mapeo_archivos.get(carrera_seleccionada)
        
        # Debug: mostrar ruta actual y archivos disponibles
        ruta_actual = 'OneDrive/Desktop/Malla interactiva python'
        archivos_disponibles = os.listdir(ruta_actual)
        
        print(f"Ruta actual: {ruta_actual}")
        print(f"Buscando archivo: {nombre_archivo}")
        print(f"Archivos en la carpeta: {archivos_disponibles}")
        
        if nombre_archivo and os.path.exists(nombre_archivo):
            try:
                # Ocultar ventana de inicio
                self.root.withdraw()
                # Crear nueva ventana para la malla
                ventana_malla = tk.Toplevel(self.root)
                app = MallaCurricular(ventana_malla, self.root, nombre_archivo, carrera_seleccionada)
            except Exception as e:
                self.root.deiconify()
                messagebox.showerror(
                    "Error",
                    f"Error al cargar la malla:\n{str(e)}"
                )
        else:
            messagebox.showerror(
                "Archivo no encontrado",
                f"No se encontró el archivo '{nombre_archivo}'\n\nRuta actual: {ruta_actual}\n\nArchivos JSON encontrados:\n" + 
                "\n".join([f for f in archivos_disponibles if f.endswith('.json')])
            )


class MallaCurricular:
    def __init__(self, root, ventana_principal, archivo_malla, nombre_carrera):
        self.root = root
        self.ventana_principal = ventana_principal
        self.archivo_malla = archivo_malla
        self.nombre_carrera = nombre_carrera
        self.root.title(f"Malla Curricular - {nombre_carrera}")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        
        # Al cerrar la ventana de malla, volver a la ventana principal
        self.root.protocol("WM_DELETE_WINDOW", self.volver_inicio)
        
        # Diccionario para almacenar el estado de las materias (aprobadas o no)
        self.materias_aprobadas = set()
        self.botones = {}
        
        # Cargar la malla desde el archivo
        self.cargar_malla_desde_archivo()
        
        self.crear_interfaz()
    
    def cargar_malla_desde_archivo(self):
        """Carga la información de la malla desde un archivo JSON"""
        try:
            with open(self.archivo_malla, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.prerequisitos = data.get('prerequisitos', {})
                # Convertir las listas a tuplas para mantener compatibilidad con el resto del código
                malla_raw = data.get('malla', {})
                self.malla = {}
                for semestre, materias in malla_raw.items():
                    self.malla[semestre] = [tuple(materia) for materia in materias]
        except Exception as e:
            # Si falla la carga, usar valores por defecto (malla de sistemas hardcoded)
            messagebox.showwarning(
                "Advertencia",
                f"No se pudo cargar el archivo. Usando malla por defecto.\nError: {str(e)}"
            )
            self.prerequisitos = {
                "Calculo 2": ["Calculo 1"],
                "Calculo 3": ["Algebra lineal", "Calculo 2"],
                "Fisica mecanica": ["Calculo 1"],
                "Fisica calor ondas": ["Calculo 1", "Fisica mecanica"],
                "Fisica electricidad": ["Calculo 2", "Fisica mecanica"],
                "Algoritmia y programacion 2": ["Algoritmia y programacion 1"],
                "Competencias comunicativas 2": ["Competencias comunicativas 1"],
                "Ingles 2": ["Ingles 1"],
                "Ingles 3": ["Ingles 2"],
                "Ingles 4": ["Ingles 3"],
                "Ingles 5": ["Ingles 4"],
                "Ingles 6": ["Ingles 5"],
                "Ingles 7": ["Ingles 6"],
                "Ingles 8": ["Ingles 7"],
                "Ecuaciones Diferenciales": ["Calculo 2"],
                "Analisis de datos": ["Calculo 2"],
                "Estructuras de datos 1": ["Algoritmia y programacion 2"],
                "POO": ["Algoritmia y programacion 2"],
                "Estructuras de datos 2": ["Estructuras de datos 1"],
                "Examen comprehensivo 1": ["Ecuaciones Diferenciales", "Calculo 3", "Fisica mecanica", "Fisica calor ondas", "Fisica electricidad"],
                "Compiladores": ["POO", "Estructuras de datos 2"],
                "Soluciones computacionales": ["Ecuaciones Diferenciales"],
                "Algoritmos y complejidad": ["Estructuras de datos 2"],
                "Estructuras discretas": ["Matematicas discretas"],
                "Diseño digital": ["Matematicas discretas"],
                "Optimizacion": ["Analisis de datos", "Soluciones computacionales"],
                "Bases de datos": ["Algoritmos y complejidad"],
                "Estructura del computador 1": ["Diseño digital"],
                "Diseño de software 1": ["Bases de datos"],
                "Electiva en redes": ["Redes"],
                "Sistemas operativos": ["Estructura del computador 1"],
                "Estructura del computador 2": ["Estructura del computador 1"],
                "Diseño de software 2": ["Diseño de software 1"],
                "Examen comprehensivo 2": ["Examen comprehensivo 1"],
                "Proyecto final": ["Diseño de software 2", "Examen comprehensivo 2", "Ingles 8"]
            }
            
            self.malla = {
                "I": [
                    ("Algebra lineal", 3),
                    ("Calculo 1", 5),
                    ("Introduccion a la ingenieria de sistemas", 1),
                    ("Algoritmia y programacion 1", 3),
                    ("Competencias comunicativas 1", 3),
                    ("Ingles 1", 0)
                ],
                "II": [
                    ("Electiva historia", 3),
                    ("Calculo 2", 4),
                    ("Fisica mecanica", 4),
                    ("Algoritmia y programacion 2", 3),
                    ("Competencias comunicativas 2", 3),
                    ("Ingles 2", 0)
                ],
                "III": [
                    ("Electiva humanidades", 3),
                    ("Calculo 3", 4),
                    ("Fisica calor ondas", 4),
                    ("Estructuras de datos 1", 3),
                    ("POO", 3),
                    ("Ingles 3", 0)
                ],
                "IV": [
                    ("Electiva ciencias de la vida", 3),
                    ("Ecuaciones Diferenciales", 3),
                    ("Fisica electricidad", 4),
                    ("Estructuras de datos 2", 3),
                    ("Matematicas discretas", 3),
                    ("Ingles 4", 0),
                    ("Seminario de carrera 1", 0)
                ],
                "V": [
                    ("Electiva ciencias basicas", 3),
                    ("Analisis de datos", 4),
                    ("Algoritmos y complejidad", 3),
                    ("Estructuras discretas", 3),
                    ("Diseño digital", 3),
                    ("Ingles 5", 0),
                    ("Examen comprehensivo 1", 0)
                ],
                "VI": [
                    ("Electiva basica profesional", 3),
                    ("Soluciones computacionales", 3),
                    ("Bases de datos", 3),
                    ("Redes", 3),
                    ("Estructura del computador 1", 3),
                    ("Ingles 6", 0)
                ],
                "VII": [
                    ("Electiva etica", 3),
                    ("Optimizacion", 3),
                    ("Diseño de software 1", 3),
                    ("Sistemas operativos", 3),
                    ("Estructura del computador 2", 3),
                    ("Ingles 7", 0)
                ],
                "VIII": [
                    ("Electiva en redes", 2),
                    ("Electiva profesional 1", 3),
                    ("Diseño de software 2", 3),
                    ("Electiva sociales", 3),
                    ("Compiladores", 3),
                    ("Ingles 8", 0),
                    ("Electiva innovacion", 3)
                ],
                "IX": [
                    ("Electiva en ciencias computacion", 3),
                    ("Electiva profesional 2", 3),
                    ("Electiva en filosofia", 3),
                    ("Electiva gestion informatica", 3),
                    ("Electiva formacion complementaria 1", 3),
                    ("Examen comprehensivo 2", 0),
                    ("Seminario de carrera 2", 0)
                ],
                "X": [
                    ("Electiva en estudios del caribe", 3),
                    ("Electiva profesional 3", 3),
                    ("Proyecto final", 3),
                    ("Electiva formacion complementaria 2", 3)
                ]
            }
    
    def volver_inicio(self):
        """Cierra la ventana de malla y vuelve a mostrar la ventana de inicio"""
        self.root.destroy()
        self.ventana_principal.deiconify()
    
    def crear_interfaz(self):
        # Frame principal con scroll
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        # Crear las columnas de semestres
        for col_idx, (semestre, materias) in enumerate(self.malla.items()):
            # Header del semestre (clickeable para aprobar todo el semestre)
            header = tk.Button(
                scrollable_frame,
                text=semestre,
                font=('Arial', 14, 'bold'),
                bg='#4a90e2',
                fg='white',
                padx=20,
                pady=10,
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2',
                command=lambda s=semestre: self.aprobar_semestre(s)
            )
            header.grid(row=0, column=col_idx, padx=5, pady=5, sticky='ew')
            
            # Botones de materias
            for row_idx, (materia, creditos) in enumerate(materias, start=1):
                btn = tk.Button(
                    scrollable_frame,
                    text=f"{materia}\n({creditos} créditos)" if creditos > 0 else materia,
                    width=18,
                    height=4,
                    font=('Arial', 8),
                    bg='white',
                    relief=tk.RAISED,
                    borderwidth=2,
                    cursor='hand2',
                    wraplength=120
                )
                btn.configure(command=lambda m=materia, b=btn: self.toggle_materia(m, b))
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                self.botones[materia] = btn
        
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        
        # Frame de botones inferiores
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(side=tk.BOTTOM, pady=30)
        
        btn_regresar = tk.Button(
            button_frame,
            text="Regresar",
            font=('Arial', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            padx=30,
            pady=10,
            command=self.volver_inicio,
            cursor='hand2'
        )
        btn_regresar.pack(side=tk.LEFT, padx=10)
        
        btn_limpiar = tk.Button(
            button_frame,
            text="Limpiar",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=30,
            pady=10,
            command=self.limpiar_progreso,
            cursor='hand2'
        )
        btn_limpiar.pack(side=tk.LEFT, padx=10)
        
        btn_guardar = tk.Button(
            button_frame,
            text="Guardar Progreso",
            font=('Arial', 12, 'bold'),
            bg='#2ecc71',
            fg='white',
            padx=30,
            pady=10,
            command=self.guardar_progreso,
            cursor='hand2'
        )
        btn_guardar.pack(side=tk.LEFT, padx=10)
        
        btn_estadisticas = tk.Button(
            button_frame,
            text="Ver Estadísticas",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=30,
            pady=10,
            command=self.mostrar_estadisticas,
            cursor='hand2'
        )
        btn_estadisticas.pack(side=tk.LEFT, padx=10)
        
        # Actualizar colores iniciales
        self.actualizar_colores()
    
    def aprobar_semestre(self, semestre):
        """Aprueba todas las materias disponibles de un semestre completo"""
        materias_semestre = [materia for materia, _ in self.malla[semestre]]
        
        # Separar materias en disponibles y bloqueadas
        materias_disponibles = []
        materias_bloqueadas = []
        
        for materia in materias_semestre:
            if materia not in self.materias_aprobadas:
                if self.puede_cursar(materia):
                    materias_disponibles.append(materia)
                else:
                    materias_bloqueadas.append(materia)
        
        # Si no hay materias para aprobar
        #if not materias_disponibles and not materias_bloqueadas:
            #messagebox.showinfo(
                #"Semestre completo",
                #f"Ya tienes todas las materias del semestre {semestre} aprobadas."
           # )
            #return
        
        # Si hay materias bloqueadas, informar al usuario
        if materias_bloqueadas:
            mensaje = f"Del semestre {semestre}:\n\n"
            if materias_disponibles:
                mensaje += f" Se aprobarán {len(materias_disponibles)} materias disponibles\n"
                mensaje += f" {len(materias_bloqueadas)} materias están bloqueadas por falta de prerequisitos\n\n"
                mensaje += "Materias bloqueadas:\n"
                mensaje += "\n".join(f"  • {m}" for m in sorted(materias_bloqueadas)[:5])
                if len(materias_bloqueadas) > 5:
                    mensaje += f"\n  ... y {len(materias_bloqueadas) - 5} más"
            else:
                mensaje += "Las siguientes materias están bloqueadas por falta de prerequisitos:\n\n"
                mensaje += "\n".join(f"  • {m}" for m in sorted(materias_bloqueadas))
                messagebox.showwarning("No se puede aprobar el semestre", mensaje)
                return
            
            messagebox.showinfo("Aprobación parcial del semestre", mensaje)
        
        # Aprobar solo las materias disponibles
        for materia in materias_disponibles:
            self.materias_aprobadas.add(materia)
        
        self.actualizar_colores()
        
        # Mensaje de confirmación
        #if materias_disponibles:
            #messagebox.showinfo(
                #"Materias aprobadas",
                #f"✅ Se aprobaron {len(materias_disponibles)} materias del semestre {semestre}"
            #)
    
    def puede_cursar(self, materia):
        """Verifica si se pueden cursar una materia (prerequisitos cumplidos)"""
        if materia not in self.prerequisitos:
            return True
        return all(prereq in self.materias_aprobadas for prereq in self.prerequisitos[materia])
    
    def toggle_materia(self, materia, boton):
        """Cambia el estado de una materia (aprobada/no aprobada)"""
        if materia in self.materias_aprobadas:
            # Encontrar todas las materias que dependen directa o indirectamente de esta
            dependientes = self.obtener_dependientes_recursivo(materia)
            
            #if dependientes:
                #Mostrar advertencia con todas las materias que se desmarcarán
                #mensaje = f"Al desmarcar '{materia}' también se desmarcarán:\n\n"
                #mensaje += "\n".join(f"• {dep}" for dep in sorted(dependientes))
                #mensaje += "\n\n¿Deseas continuar?"
                
                #if not messagebox.askyesno("Desmarcar materias en cadena", mensaje):
                 #   return
            
            # Desmarcar la materia actual y todas sus dependientes
            self.materias_aprobadas.remove(materia)
            for dep in dependientes:
                if dep in self.materias_aprobadas:
                    self.materias_aprobadas.remove(dep)
        else:
            # Verificar prerequisitos
            if not self.puede_cursar(materia):
                faltantes = [p for p in self.prerequisitos[materia] 
                           if p not in self.materias_aprobadas]
                messagebox.showwarning(
                    "Prerequisitos no cumplidos",
                    f"Para cursar {materia} necesitas aprobar:\n" + 
                    "\n".join(f"• {p}" for p in faltantes)
                )
                return
            
            self.materias_aprobadas.add(materia)
        self.actualizar_colores()
    
    def obtener_dependientes_recursivo(self, materia):
        """Obtiene todas las materias que dependen directa o indirectamente de una materia"""
        dependientes = set()
        
        # Buscar materias que tienen a 'materia' como prerequisito directo
        for m, prereqs in self.prerequisitos.items():
            if materia in prereqs and m in self.materias_aprobadas:
                dependientes.add(m)
                # Recursivamente obtener los dependientes de esta materia
                sub_dependientes = self.obtener_dependientes_recursivo(m)
                dependientes.update(sub_dependientes)
        
        return dependientes
    
    def actualizar_colores(self):
        """Actualiza los colores de todos los botones según su estado"""
        for materia, boton in self.botones.items():
            if materia in self.materias_aprobadas:
                # Aprobada - Verde
                boton.configure(bg='#2ecc71', fg='white', font=('Arial', 8))
            elif self.puede_cursar(materia):
                # Disponible - Blanco
                boton.configure(bg='white', fg='black', font=('Arial', 8))
            else:
                # Bloqueada - Gris
                boton.configure(bg='#bdc3c7', fg='#7f8c8d', font=('Arial', 8))
    
    def limpiar_progreso(self):
        """Limpia todo el progreso"""
        #if messagebox.askyesno("Confirmar", "¿Estás seguro de limpiar todo el progreso?"):
        self.materias_aprobadas.clear()
        self.actualizar_colores()
    
    def guardar_progreso(self):
        """Guarda el progreso en un archivo JSON"""
        with open('progreso_malla.json', 'w') as f:
            json.dump(list(self.materias_aprobadas), f)
        messagebox.showinfo("Guardado", "Progreso guardado exitosamente")
    
    def cargar_progreso(self):
        """Carga el progreso desde un archivo JSON"""
        if os.path.exists('progreso_malla.json'):
            try:
                with open('progreso_malla.json', 'r') as f:
                    self.materias_aprobadas = set(json.load(f))
                self.actualizar_colores()
            except:
                pass
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del progreso"""
        total_materias = len(self.botones)
        aprobadas = len(self.materias_aprobadas)
        porcentaje = (aprobadas / total_materias) * 100
        
        # Calcular créditos
        creditos_totales = 0
        creditos_aprobados = 0
        for semestre, materias in self.malla.items():
            for materia, creditos in materias:
                creditos_totales += creditos
                if materia in self.materias_aprobadas:
                    creditos_aprobados += creditos
        
        # Materias disponibles para cursar
        disponibles = [m for m in self.botones.keys() 
                      if m not in self.materias_aprobadas and self.puede_cursar(m)]
        
        mensaje = f"""
📊 ESTADÍSTICAS DE PROGRESO

Materias aprobadas: {aprobadas}/{total_materias}
Progreso: {porcentaje:.1f}%

Créditos aprobados: {creditos_aprobados}/{creditos_totales}
Créditos completados: {(creditos_aprobados/creditos_totales*100):.1f}%

Materias disponibles para cursar: {len(disponibles)}

{chr(10).join(f"  • {d}" for d in disponibles[:10])}
{"  ..." if len(disponibles) > 10 else ""}
        """
        messagebox.showinfo("Estadísticas", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root)
    root.mainloop()