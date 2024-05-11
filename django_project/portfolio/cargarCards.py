from portfolio.models import Proyecto
p1=Proyecto(titulo='SGI de Pozos Petroleros', descripcion='Plataforma web para la gestion de datos de pozos petroleros de estacion Caimancito', tecnologias='SQL Server, ASP, Codecharge', link='https://www.lanacion.com', imagen='img/pozos.png')
p1.save()
p4=Proyecto(titulo="SGI Toners y Reciclados", descripcion="Aplicacion de escritorio para la gestion de reciclados de toner de ECIN", tecnologias="VB SQL", link="https://www.ecinsoluciones.com", imagen="img/ecin.png")
p4.save()
p3=Proyecto(titulo="IA para identificación de personas", descripcion="Plataforma web para la identificacion de personas a traves de la palma de la mano", tecnologias="Django Python GPU MySQL", link="#", imagen="img/IA.png")
p3.save()
