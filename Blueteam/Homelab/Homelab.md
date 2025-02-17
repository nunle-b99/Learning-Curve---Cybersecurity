# HOMELAB
Das Erstellen eines Homelabs ist eine gute Möglichkeit die Fähigkeiten der Redteam Übungen zu testen, aber auch mehr über Verteidigungsmechanismen zu lernen. Inspiriert ist das Homelab von folgendem Beitrag: [Medium.com - Author: josegpac](https://medium.com/@josegpach/embarking-on-a-cybersecurity-journey-my-home-lab-setup-6f06b454cb75)

Hardware die ich Zuhause besitze und für das Netzwerk benötige:
- "Standard" Telekom Router
- PC, auf denen alle Virtualisierungen laufen werden
- Heimnetzwerk: Notebook, FireTV ...

Mir ist wichtig, dass das Heimnetzwerk möglichst unverändert bleibt. Dazu wollte ich das Netzwerk in ein privates Subnet und ein test Subnet aufteilen. Dies ist jedoch mit meiner Hardware nict möglich und nur durch den Kauf von zusätzlicher Hardware machbar. Die Ausweichmethode ist die Verwendung einer virtuellen pfsense-Maschine. Daran angeschlossene Verbindungen können in Subnets augeteilt werden (vgl. Abbildung).  

<p align="center">
  <img src="https://github.com/user-attachments/assets/b33dfa2f-5cd1-4d88-a14f-4370a2fe2c4f">
</p>


