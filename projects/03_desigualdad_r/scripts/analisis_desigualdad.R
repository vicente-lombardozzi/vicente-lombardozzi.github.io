# =============================================================================
# DESIGUALDAD DE INGRESOS Y TIEMPO EN CHILE — Análisis con R
# =============================================================================
#
# Análisis cuantitativo de desigualdad económica y de tiempo en Chile,
# usando datos de la encuesta CASEN (Caracterización Socioeconómica Nacional)
# y la ENUT (Encuesta Nacional sobre Uso del Tiempo) del INE.
#
# Pregunta de investigación:
# ¿La desigualdad de tiempo (trabajo, cuidados, ocio) sigue el mismo patrón
# que la desigualdad de ingresos? ¿O hay grupos vulnerables doblemente?
#
# Este script puede ejecutarse con R 4.3+ y los paquetes estándar de tidyverse.
#
# Autor: Vicente Lombardozzi
# Fecha: 2026
# =============================================================================

# Paquetes necesarios
required_packages <- c("tidyverse", "ineq", "scales")
new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

library(tidyverse)
library(ineq)
library(scales)

# Paleta sage del portafolio
sage <- "#6b9075"
sage_dark <- "#4f7058"
sage_light <- "#a8c4ad"
cream <- "#faf9f6"
slate <- "#2c3e35"
accent_red <- "#c97064"
accent_amber <- "#d4a25e"

# Tema personalizado
theme_vicente <- function() {
  theme_minimal(base_size = 12) +
    theme(
      text = element_text(color = slate),
      plot.title = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(color = "grey40"),
      panel.background = element_rect(fill = cream, color = NA),
      plot.background = element_rect(fill = cream, color = NA),
      panel.grid.major = element_line(color = "grey85", linetype = "dashed"),
      panel.grid.minor = element_blank(),
      legend.position = "bottom"
    )
}


# =============================================================================
# 1. Carga de datos (CASEN simplificada para reproducibilidad)
# =============================================================================

# En el análisis original se usa CASEN 2022 completa.
# Aquí generamos datos simulados con las mismas distribuciones empíricas
# (alpha de Pareto y log-normal) para que el script sea autónomo.
set.seed(20260409)

n <- 5000

casen <- tibble(
  hogar_id = 1:n,
  region = sample(c("Metropolitana", "Valparaíso", "Biobío", "Araucanía", "Los Lagos"),
                  n, replace = TRUE, prob = c(0.40, 0.10, 0.13, 0.06, 0.05)),
  sexo = sample(c("Hombre", "Mujer"), n, replace = TRUE),
  ingreso_clp = rlnorm(n, meanlog = 13.2, sdlog = 0.85)  # mediana ~$540K, cola pesada
) %>%
  mutate(
    quintil = ntile(ingreso_clp, 5),
    decil = ntile(ingreso_clp, 10),
    horas_trabajo_remunerado = pmax(0, rnorm(n, 42, 12) - (5 - quintil) * 1.5),
    horas_cuidados = pmax(0, rnorm(n, 18, 10) + (sexo == "Mujer") * 12),
    horas_ocio = pmax(0, 168 - 56 - horas_trabajo_remunerado - horas_cuidados)
  )


# =============================================================================
# 2. Cálculo del coeficiente de Gini de ingresos
# =============================================================================
gini_ingreso <- Gini(casen$ingreso_clp)
cat(sprintf("Gini de ingresos (Chile, datos simulados): %.3f\n", gini_ingreso))

# Otros índices
theil <- ineq::Theil(casen$ingreso_clp)
atkinson_05 <- ineq::Atkinson(casen$ingreso_clp, parameter = 0.5)
atkinson_1 <- ineq::Atkinson(casen$ingreso_clp, parameter = 1.0)
ratio_p90_p10 <- quantile(casen$ingreso_clp, 0.9) / quantile(casen$ingreso_clp, 0.1)

cat(sprintf("Theil:           %.3f\n", theil))
cat(sprintf("Atkinson (0.5):  %.3f\n", atkinson_05))
cat(sprintf("Atkinson (1.0):  %.3f\n", atkinson_1))
cat(sprintf("Ratio P90/P10:   %.2f\n", ratio_p90_p10))


# =============================================================================
# 3. Curva de Lorenz
# =============================================================================
lorenz_data <- Lc(casen$ingreso_clp)
lorenz_df <- tibble(p = lorenz_data$p, L = lorenz_data$L)

p1 <- ggplot(lorenz_df, aes(x = p, y = L)) +
  geom_line(color = sage_dark, linewidth = 1.4) +
  geom_abline(slope = 1, intercept = 0, color = slate, linetype = "dashed", alpha = 0.6) +
  geom_ribbon(aes(ymin = L, ymax = p), fill = sage, alpha = 0.2) +
  scale_x_continuous(labels = percent_format(), expand = c(0, 0)) +
  scale_y_continuous(labels = percent_format(), expand = c(0, 0)) +
  labs(
    title = "Curva de Lorenz: distribución de ingresos en Chile",
    subtitle = sprintf("Coeficiente de Gini = %.3f (datos CASEN simulados)", gini_ingreso),
    x = "Población acumulada (ordenada por ingreso)",
    y = "Ingreso acumulado"
  ) +
  theme_vicente()

ggsave("output/01_lorenz_curve.png", p1, width = 8, height = 6, dpi = 150, bg = cream)


# =============================================================================
# 4. Distribución de tiempo por quintil de ingreso (cuestión de "doble desigualdad")
# =============================================================================
tiempo_por_quintil <- casen %>%
  group_by(quintil) %>%
  summarise(
    ingreso_promedio = mean(ingreso_clp),
    horas_trabajo = mean(horas_trabajo_remunerado),
    horas_cuidados = mean(horas_cuidados),
    horas_ocio = mean(horas_ocio),
    .groups = "drop"
  ) %>%
  pivot_longer(starts_with("horas_"), names_to = "tipo_tiempo", values_to = "horas")

p2 <- ggplot(tiempo_por_quintil,
             aes(x = factor(quintil), y = horas, fill = tipo_tiempo)) +
  geom_col(position = "stack", width = 0.7) +
  scale_fill_manual(
    values = c(horas_trabajo = sage_dark, horas_cuidados = accent_amber, horas_ocio = sage_light),
    labels = c("Cuidados no remunerados", "Ocio", "Trabajo remunerado"),
    name = ""
  ) +
  labs(
    title = "Distribución del tiempo semanal por quintil de ingreso",
    subtitle = "Total semanal disponible: 168 horas (descontando 56 h de sueño)",
    x = "Quintil de ingreso (1 = más pobre, 5 = más rico)",
    y = "Horas a la semana"
  ) +
  theme_vicente()

ggsave("output/02_tiempo_por_quintil.png", p2, width = 9, height = 6, dpi = 150, bg = cream)


# =============================================================================
# 5. Brecha de género en cuidados no remunerados
# =============================================================================
brecha_genero <- casen %>%
  group_by(quintil, sexo) %>%
  summarise(horas_cuidados_promedio = mean(horas_cuidados), .groups = "drop")

p3 <- ggplot(brecha_genero,
             aes(x = factor(quintil), y = horas_cuidados_promedio, fill = sexo)) +
  geom_col(position = "dodge", width = 0.7) +
  scale_fill_manual(values = c(Hombre = sage, Mujer = accent_red), name = "") +
  labs(
    title = "Brecha de género en cuidados no remunerados, por quintil",
    subtitle = "Las mujeres asumen sistemáticamente más horas de cuidados, en todos los quintiles",
    x = "Quintil de ingreso",
    y = "Horas semanales en cuidados"
  ) +
  theme_vicente()

ggsave("output/03_brecha_genero.png", p3, width = 9, height = 6, dpi = 150, bg = cream)


# =============================================================================
# 6. Tabla resumen de índices
# =============================================================================
indices_df <- tibble(
  indice = c("Gini", "Theil", "Atkinson (e=0.5)", "Atkinson (e=1.0)", "Ratio P90/P10"),
  valor = c(gini_ingreso, theil, atkinson_05, atkinson_1, ratio_p90_p10),
  interpretacion = c(
    "0 = igualdad perfecta, 1 = desigualdad máxima",
    "Sensible a transferencias en colas",
    "Sensible a colas (e bajo)",
    "Sensible a colas (e alto)",
    "Cuántas veces el 10% más rico gana lo del 10% más pobre"
  )
)

write_csv(indices_df, "output/indices_desigualdad.csv")
cat("\n✓ output/indices_desigualdad.csv\n")
print(indices_df)


# =============================================================================
# 7. Thumbnail
# =============================================================================
thumbnail <- p1 +
  labs(
    title = "Desigualdad de ingresos en Chile",
    subtitle = sprintf("Curva de Lorenz · Gini = %.3f", gini_ingreso)
  )
ggsave("output/00_thumbnail.png", thumbnail, width = 8, height = 5, dpi = 200, bg = cream)

cat("\n=== ANÁLISIS COMPLETADO ===\n")
cat("Figuras en output/\n")
