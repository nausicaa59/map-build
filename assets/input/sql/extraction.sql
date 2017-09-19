#extraction
select 
	pseudo, 
	nb_messages,
	IF(date_inscription = "0000-00-00",0, DATEDIFF(CURDATE(),date_inscription)) AS nb_jours
FROM auteurs
ORDER BY pseudo ASC