SELECT * FROM battles ;
SELECT * FROM death2 ;
SELECT * FROM deaths ;
SELECT * FROM predictions ;
SELECT * FROM tv_stats ;

-- pour la route /character
SELECT p.name, p.title, p.culture, p.house, p.dateOfBirth, p.DateoFdeath,
CASE 
	WHEN p.DateoFdeath is null
		then 'Alive'
	else 'Dead'
end as dead_or_not
FROM predictions as p ;

-- pour la route /character/character_id
SELECT
    p.character_id,
    p.name,
    p.title,
    p.culture,
    p.house,
    p.dateOfBirth,
    p.DateoFdeath,
    p.father,
    p.mother,
    p.heir,
    p.spouse,
    CASE
        WHEN p.DateoFdeath IS NULL THEN 'Alive'
        ELSE 'Dead'
    END AS dead_or_not,
    CASE
        WHEN p.DateoFdeath IS NOT NULL THEN p.DateoFdeath - p.dateOfBirth
        ELSE NULL
    END AS Age,
    CASE
        WHEN d2.book_of_death = '1' THEN 'a_game_of_thrones'
        WHEN d2.book_of_death = '2' THEN 'a_clash_of_kings'
        WHEN d2.book_of_death = '3' THEN 'a_storm_of_swords'
        WHEN d2.book_of_death = '4' THEN 'a_feast_for_crows'
        WHEN d2.book_of_death = '5' THEN 'a_dance_with_dragons'
        ELSE NULL
    END AS Book_of_dead
FROM predictions AS p
LEFT JOIN death2 AS d2 ON d2.name = p.name
;

-- verifier les données 'book'
select 	p.character_id, 
		p.name,
        p.book1,
        p.book2,
        p.book3,
        p.book4,
        p.book5,
        d.GoT,
        d.CoK,
        d.SoS,
        d.FfC,
        d.DwD,
        d2.book_of_death,
        d2.a_game_of_thrones,
        d2.a_clash_of_kings,
        d2.a_storm_of_swords,
        d2.a_feast_for_crows,
        d2.a_dance_with_dragons
FROM predictions as p
INNER JOIN deaths as d on p.name = d.name
INNER JOIN death2 as d2 on d2.name = p.name ;

