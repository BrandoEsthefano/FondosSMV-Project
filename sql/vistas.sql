
USE SMV_FONDOS

---------------------------------------------------------------------------------

SELECT * FROM fact_fondos
SELECT * FROM vista_fondos_activos
SELECT * FROM vista_fondos_sin_datos
SELECT * FROM vista_resumen_mensual
SELECT * FROM vista_ultimo_snapshot_V2


-- FONDOS ACTIVOS

CREATE VIEW vista_fondos_activos AS
SELECT F.id_fondo, A.RazonSocial, F.DenominacionFondo, F.TipoFondo, F.FechaInscripcion, F.ResolucionInscripcion, F.Moneda, F.FechaInformacion, F.PatrimonioInscrito, F.ValorCuota,
	F.NumeroParticipes, F.NumeroCuotas,

	CASE 
		WHEN F.NumeroParticipes > 0 THEN F.PatrimonioInscrito / F.NumeroParticipes ELSE NULL END AS PatrimonioPromedioPorParticipe,
	DATEDIFF(YEAR, F.FechaInscripcion, GETDATE()) AS AñosDelFondo,
	F.FechaCarga, FORMAT(F.FechaInformacion, 'yyyy-MM') AS PeriodoSnapshot

FROM fact_fondos F
JOIN dim_administradoras A ON F.idAdministradora = A.idAdministradora
WHERE TieneDatos = 1

---------------------------------------------------------------------------------

-- RESUMEN MENSUAL

CREATE VIEW vista_resumen_mensual AS
SELECT PeriodoSnapshot, TipoFondo, Moneda, COUNT(*) AS TotalFondos,
	SUM(PatrimonioInscrito) AS PatrimonioTotal,
	AVG(PatrimonioInscrito) AS PatrimonioPromedio,
	AVG(ValorCuota) AS ValorCuotaPromedio,
	SUM(NumeroParticipes) AS ParticipesTotal
FROM vista_fondos_activos
GROUP BY PeriodoSnapshot, TipoFondo, Moneda

---------------------------------------------------------------------------------

-- FONDOS SIN DATOS

ALTER VIEW vista_fondos_sin_datos AS
SELECT DenominacionFondo ,TipoFondo, Moneda, FechaInscripcion, AnioInscripcion, 
	DATEDIFF(DAY, FechaInscripcion, GETDATE()) AS DiasDesdeInscripcion,
	FechaCarga,
	FORMAT(FechaInformacion, 'yyyy-MM') AS PeriodoSnapshot
FROM fact_fondos
WHERE TieneDatos = 0

---------------------------------------------------------------------------------

-- ULTIMO SNAPSHOT (MODIFICADO)

ALTER VIEW vista_ultimo_snapshot_V2 AS
SELECT F.id_fondo, A.idAdministradora, F.DenominacionFondo, F.TipoFondo, F.FechaInscripcion, F.ResolucionInscripcion, F.Moneda, F.FechaInformacion, F.PatrimonioInscrito, F.ValorCuota,
	F.NumeroParticipes ,F.NumeroCuotas, F.AnioInscripcion, F.TieneDatos, F.FechaCarga
FROM fact_fondos F
JOIN dim_administradoras A ON F.idAdministradora = A.idAdministradora
WHERE FechaCarga = (SELECT MAX(FechaCarga) FROM fact_fondos)

---------------------------------------------------------------------------------




 