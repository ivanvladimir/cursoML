#include <stdio.h>
#include <vector>
#include <map>
#include <stack>
#include <iostream>

#define ROWS 0 
#define COLS 1

/*
 * Al ejecutar la funcion principal( hungarianAlgorithm), devuelve un vector donde cada indice del vector
 * representa a un empleado y cada valor del vector representa la tarea que le fue asignada,
 * si el valor es -1, se trata de un error interno del algoritmo y se trataria de un bug en el programa.
 * Si devuelve -2 el empleado no tiene una tarea asignada ya que todas las tareas han sido asignadas a otros empleados.
 *
 */
template <class T, class U>
class Hungarian
{
public:
     std::vector<std::vector <float> > cost_matrix; //Matrix of costs between people and activities
     std::vector<std::vector <float> > copy_cost_matrix;//Matrix copy without changes
     std::vector <int> assigned_activities; // final relation, what people must do what activity
     int size_p, size_a;
	
     //constructor	
     Hungarian(const std::vector<T> people, const std::vector<U> activities, float (*cost_function)(T, U))
	  {
	       int a, mayor = 0;
	       size_p = people.size();
	       size_a = activities.size();
	   
	       // fill the cost matrix
	       for(int i = 0; i < people.size(); ++i)
	       {
		    std::vector<float> aux;
		    for(int j = 0; j < activities.size(); ++j)
		    {
			 aux.push_back((*cost_function)(people[i], activities[j]));
			 if (aux[j] > mayor)
			      mayor = aux[j];
		    }
		    cost_matrix.push_back(aux);
	       }				

	       // make cost matrix nxn by adding max value as extra element
	       if(people.size() < activities.size())
	       {
		    a = activities.size() - people.size();
		    for(int i = 0; i < a; ++i)
		    {
			 std::vector<float> aux;
			 for(int j = 0; j < activities.size(); ++j)
			      aux.push_back(mayor);
			 cost_matrix.push_back(aux);
		    }
					
	       }
	       else if(people.size() > activities.size())
	       {	
		    a = people.size() - activities.size();
		    for(int i = 0; i < a; ++i)
			 for(int j = 0; j < people.size(); ++j)
			      cost_matrix[j].push_back(mayor);
	       }
	  }
				
     bool find(const std::vector <int> A, float value)
	  {
	       for(int i = 0; i < A.size(); ++i)
		    if(A[i] == value)
			 return true;

	       return false;
	  }
		
     bool find(std::map <int, int> A, int value)
	  {
	       std::map<int,int>::iterator val;
	       for(int i = 0; i < A.size(); ++i)
		    if(A[i] == value)
			 return true;

	       return false;
	  }
		
     int findMinimum(std::vector <float> A)
	  {
	       int i;
	       float min = 100000;
	       for(int i = 0; i < A.size(); ++i)
		    if(A[i] < min)
			 min = A[i];
	       return min;
	  }
		
     void reduceRows()
	  {
	       float min;
	       for(int i = 0; i < cost_matrix.size(); ++i)
	       {
		    min = findMinimum(cost_matrix[i]);
		    for(int j = 0; j < cost_matrix.size(); ++j)
			 cost_matrix[i][j] -= min;
	       }
	  }
		
     void reduceColumns()
	  {
	       float min;
	       for(int i = 0; i < cost_matrix.size(); ++i)
	       {
		    min = 100000;
		    for(int j = 0; j < cost_matrix.size(); ++j)
			 if(cost_matrix[j][i] < min)
			      min = cost_matrix[j][i];

		    for(int j = 0; j < cost_matrix.size(); ++j)
			 cost_matrix[j][i] -= min;
	       }
	  }
		
     int countOnesNeg(std::vector <int> v)
	  {
	       int count = 0;
	       for(int i = 0; i < v.size(); ++i)
		    if(v[i] == -1)
			 count++;

	       return count;
	  }
		
     float calculateCost(std::vector<int> v)
	  {
	       float cost = 0;
	       for(int i = 0; i < cost_matrix.size(); ++i)
		    if(v[i] != -1)
			 cost += copy_cost_matrix[i][v[i]];

	       return cost;
						
	  }
		
     std::vector<int> assign_activities()
	  {
	       //En este caso el conjunto A son los renglones y B son las columnas
	       int M_cost = 1000000;
	       std::vector <int> M (4,-1);
	       std::vector < std::vector <int> > unionsAB;

	       //construccion del vector de uniones. Contendra las uniones entre los conjuntos A y B
	       for(int i = 0; i < cost_matrix.size(); ++i)
	       {
		    unionsAB.push_back(std::vector <int> (0));
		    for(int j = 0; j < cost_matrix.size(); ++j)
			 if(!cost_matrix[i][j])
			      unionsAB[i].push_back(j);
	       }
	
	       for(int i = 0; i < unionsAB.size(); ++i) //recorrer el vector del conjunto A
	       {
		    for(int j = 0; j < unionsAB[i].size(); ++j) // recorre el vector de uniones de A con B
		    {
			 std::vector <int> Maux (cost_matrix.size(), -1);
			 if(!find(Maux, unionsAB[i][j])) // si no esta en el vector de asignaciones(Maux) se agrega
			 {
			      Maux[i] = (unionsAB[i][j]);     //cambia solo una union
				
			      //se recorre el arrreglo para averiguar si existen caminos adicionales
			      for(int k = 0; k < unionsAB.size(); k++) 
				   for (int f = 0; f < unionsAB[k].size(); f++)
					if(!find(Maux, unionsAB[k][f]) && i != k)
					{ 
					     Maux[k] = (unionsAB[k][f]);
					     break; ///al momento de encontrar un valor valido, sale del ciclo
					}

			      if(countOnesNeg(Maux) == countOnesNeg(M) && calculateCost(Maux) < M_cost)
			      {
				   M = Maux;
				   M_cost = calculateCost(M);
			      }

			      if(countOnesNeg(Maux) < countOnesNeg(M))
			      {
				   M = Maux;
				   M_cost = calculateCost(M);
			      }
			 }
		    }
	       }

	       return M;
	  }
		
     void coverLines(std::vector <int>& l1, std::vector <int>& l2)
	  {
	       int aux, k;
	       std::vector <int> unmarked_rows ;
	       std::vector <int> col_assigned;
	       std::vector <int> marked_rows;
	       std::vector <int> marked_cols;
	       std::vector <int> assigned_tasks;
	       // assign as many tasks as possible
	       assigned_tasks = assign_activities();
			
	       //Mark all rows having no assignments
	       for(int i = 0; i < cost_matrix.size(); ++i)
		    if(assigned_tasks[i] == -1){
			 marked_rows.push_back(i);
			 //cout << "mr: " << i << endl;
		    }
				
			
	       for(int k = 0; k < cost_matrix.size(); k++)
	       {
		    //Then mark all columns having zeros in marked row(s)
		    for(int i = 0; i < marked_rows.size(); ++i)
			 for(int j = 0; j < cost_matrix.size(); ++j)
			      if(!cost_matrix[marked_rows[i]][j] && !find(marked_cols, j))
				   marked_cols.push_back(j);

		    // Then mark all rows having assignments in marked columns
		    for(int i = 0; i < marked_cols.size(); ++i)
			 for(int j = 0; j < assigned_tasks.size(); ++j)
			      if(assigned_tasks[j] != -1)
				   if(!find(marked_rows, j) && find(marked_cols,assigned_tasks[j]))
					marked_rows.push_back(j);
	       }

	       //Now draw lines through all marked columns and unmarked rows
	       for(int i = 0; i < cost_matrix.size(); ++i)
		    if(!find(marked_rows, i))
			 unmarked_rows.push_back(i);
	       l1 = unmarked_rows;
	       l2 = marked_cols;
	  }
		
     void no_substract(int value, std::vector<int> v, int type)
	  {
	       if(!type)
	       {
		    for(int i = 0; i < cost_matrix.size(); ++i)
			 if(!find(v, i))
			      for(int j = 0; j < cost_matrix.size(); ++j)
				   cost_matrix[i][j] -= value;
	       }
	       else{
		    for(int i = 0; i < v.size(); ++i)
			 for(int j = 0; j < cost_matrix.size(); ++j)
			      cost_matrix[j][v[i]] += value;
	       }
	  }
		
     void erase_inexisting_rol()
	  {
	       if(size_a < cost_matrix.size())
	       {
		    for(int i = 0; i < assigned_activities.size(); ++i)
			 if(assigned_activities[i] >= size_a)
			      assigned_activities[i] = -2;
	       }
	       else if(size_p < cost_matrix.size())
	       {
		    for(int i = size_p; i <  assigned_activities.size(); ++i)
			 assigned_activities[i] = -2;
	       }
	  }
		
     // Principal function
     std::vector <int> hungarianAlgorithm ()
	  {
	       std::vector <int> row_lines;
	       std::vector <int> col_lines;
	       float min = 10000;

	       copy_cost_matrix = cost_matrix;
	       reduceRows();
	       reduceColumns();
	       coverLines(row_lines, col_lines);
	       while(!((row_lines.size() + col_lines.size()) == cost_matrix.size()))
	       {
		    for(int i = 0; i < cost_matrix.size(); ++i)
			 for(int j = 0; j < cost_matrix.size(); ++j)
			      if(!find(row_lines, i))
				   if(!find(col_lines, j))
					if(cost_matrix[i][j] < min)
					     min = cost_matrix[i][j];
		    no_substract(min, row_lines, ROWS);
		    no_substract(min, col_lines, COLS);
		    coverLines(row_lines, col_lines);
	       }
	       assigned_activities = assign_activities();
			
	       erase_inexisting_rol();  ///elimina las actividades o los empleados que forzaron a la matriz a ser cuadrada
			
	       return assigned_activities;
	  }
};
	      	
		
		
		

		
		
		
		
		
		
	
