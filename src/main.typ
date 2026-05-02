#import "@preview/unify:0.8.0": num, numrange, qty, qtyrange
#set text(font: "Libertinus Serif")
#set page(paper: "a4", numbering: "1")
#set text(lang: "en")
#set heading(numbering: "1.1")
#set cite(style: "american-institute-of-physics")
#set math.equation(numbering: "(1)")
#align(center)[
  #text(2em, weight: "bold")[The photoelectric effect]

  *Authors:* Filip Petrini, Markus Bajlo, Erik Miller, Simplice Alain Tatanfack \ *Date:* #datetime.today().display() \
  *Course:* Quantum Physics *1FA521* \
  *Lab:* \#3
]


= Theory
The classical interpretation of the photoelectric effect suggests that the measured photocurrent would result from exposing a material to a stream of photons, essentially charging the electron in order for it to gain enough energy to leave the material. This is, however, not observed in experiment. The fix to this discrepancy is to use the idea of quantization of energy. Photons travel as energy packets, and electrons only absorb photons that have a certain wavelength as shown in
Max Planck's equation:
$
  E = h f
$<plancks_eq>
where $h$ is Planck's constant and $f$ is the frequency of the photon. When a photon with a certain wavelength hits an electron of a similar energy level it absorbs that energy. This absorption is called "exciting" the electron and causes the electron to gain enough energy to leave the material. The amount of electrons that get emitted from the material can be measured as a current called photocurrent. That is, we measure the current of electrons that have left a material.

In reality, we also need to account for the energy needed to overcome other forces inside the material (for example, the binding energy of an atom). These are gathered in the aptly named "work function". We instead write Planck's equation as
$
  E = K_max + W_0 = h f
$<plancks_eq_with_work>
where $K_max$ is the maximum kinetic energy possible for the expelled electron and $W_0$ is the work function.

By moving around the equation above, we can find the stopping voltage as a function of the frequency of light, and likewise the work function as a function of the stopping voltage.
$
  U_s (f) = (h f)/e - W_0/e
$
$
  W_0(U_s) = h f - e U_s
$
These we can use later in our graphs to find estimates for the Planck's constant $h$ and the work function $W_0$.



@physics_handbook


= Results

== Intensity <results_a>

#figure(
  caption: [Series A current-voltage curves for three apertures at fixed wavelength. The linearized cutoff fits are shown together with the pairwise line intersections used to estimate the shared stopping voltage.],
  image("plot_a.png"),
)  <plot_a>

#figure(
  caption: [Stopping voltage measurements for the aperture series, including linear-fit intercepts and the shared intersection-based estimate. Slope values characterize the rising photocurrent region.],
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, center),
    table.hline(),
    [*Aperture (mm)*],
    [*$|U_s|$ (V)*],
    [*$d U_s$ (V)*],
    [*Slope ($10^(-11)$ A/V)*],
    [*$d("Slope")$ ($10^(-11)$ A/V)*],
    table.hline(),
    [$num("2")$],
    [$num("0.246")$],
    [$num("0.171")$],
    [$num("1.350")$],
    [$num("0.117")$],
    [$num("4")$],
    [$num("0.714")$],
    [$num("0.060")$],
    [$num("3.975")$],
    [$num("0.217")$],
    [$num("8")$],
    [$num("0.287")$],
    [$num("0.026")$],
    [$num("12.19")$],
    [$num("0.343")$],
    [Shared], [$num("0.442")$], [$num("0.456")$], [---], [---],
    table.hline(),
  ),
) <table_a>

The stopping voltages for each aperture in @plot_a and @table_a were determined by the x-intercept of a linear regression on the rising portion of the I-V curve, with the individual uncertainties $d U_s$ and $d("Slope")$ derived from the covariance matrix of each fit. The shared stopping voltage was estimated by calculating the mean of the pairwise intersection points of the three fitted lines, with its uncertainty $d U_s$ representing the standard deviation of these intersection voltages.

The results demonstrate that the stopping voltage $U_s$ theoretically should remain independent of the aperture size, whereas the slope of the photocurrent in the rising region increases significantly as the aperture is widened. This latter observation aligns with the photoelectric model: light intensity governs the rate of electron emission (photocurrent) rather than the maximum kinetic energy of the photoelectrons. However, the extracted stopping voltages show unexpected variation, notably a peak of $qty("0.714", "V")$ at the $qty("4", "mm")$ aperture compared to $qty("0.246", "V")$ and $qty("0.287", "V")$ at $qty("2", "mm")$ and $qty("8", "mm")$, respectively. This inconsistency with theory suggests significant sensitivity in the cutoff determination or potential experimental artifacts, which are addressed in @error_analysis.


== Frequency <results_b>

#figure(
  caption: [Series B current-voltage curves for three wavelengths at fixed aperture. The low-current baseline and rising region are linearly fitted and their intersections give the stopping voltages.],
  image("plot_b.png"),
) <plot_b>

The stopping voltage $U_s$ for each wavelength was determined by the intersection of a linear fit to the rising photocurrent region and a linear fit to the zero-current baseline. The uncertainties $d U_s$ were calculated by propagating the errors from the covariance matrices of the two fits and adding the squares of their standard deviations. These combined uncertainties then provided the weights for the final determination of Planck's constant. This ensures that more precise measurements have a greater influence on the extracted values of $h$ and $W_0$.

#figure(
  caption: [Extracted stopping voltage magnitudes for the wavelength series. The uncertainties include fit precision and cutoff-window sensitivity.],
  table(
    columns: (auto, auto, auto),
    align: (left, center, center),
    table.hline(),
    [*Wavelength (nm)*], [*$|U_s|$ (V)*], [*$d U_s$ (V)*],
    table.hline(),
    [$num("365")$], [$num("1.172")$], [$num("0.033")$],
    [$num("405")$], [$num("0.512")$], [$num("0.011")$],
    [$num("546")$], [$num("0.117")$], [$num("0.027")$],
    table.hline(),
  ),
) <table_b>

#figure(
  caption: [Stopping voltage magnitude against light frequency, with the weighted linear fit used to extract Planck's constant and the work function. The fit is weighted against the standard deviation of each measurement. Measurements with smaller uncertainties have larger weights.],
  image("plot_planck.png"),
) <plot_planck>

The wavelength series generally follows the expected linear trend in the photoelectric equation, although the fit is relatively weak as indicated by a coefficient of determination $R^2 = 0.746$. The fit gives a measured Planck constant of $h = qty("4.707e-34", "J s")$ and a work function of $W_0 = qty("1.601", "eV")$, with the uncertainty dominated by the spread from stopping-voltage extraction. The extracted Planck constant deviates from the accepted value by approximately $qty("29.0", "%")$, highlighting a clear discrepancy between our experimental derivation and the theoretical ideal.

The results show that there is a correlation between frequency and stopping voltage in each case. Frequency (inversely proportional to wavelength) scales proportionally with stopping voltage. This result is expected as suggested by @plancks_eq_with_work, even if the precise values exhibit unexpected deviation from accepted constants. We discuss this further in @discussion.



= Discussion <discussion>
There are two parts to the experiment. One where we vary the
aperture size, and another where we vary the wavelength (and thus the frequency) of the emitted photons. We should expect a cutoff limit to the amount of current measured as we vary the voltage as well as a larger current for some range of voltage. This is simply due to the fact that more photons of a certain wavelength hit the material by increasing the area available for the photons. The expelled electrons have different energies depending on the location of their origin (deeper into the material, for example) and their direction. A larger electrical field ensures that more electrons gain enough energy in the travel over to the detector in order to be detected. However, the cutoff limit suggests that there are only so many electrons that can be expelled from the material with photons of a certain wavelength, maxing out the possible current.

In the other part of the experiment we vary the wavelength (and thus the frequency and thus the energy) of the photons hitting the material whilst keeping the aperture size constant. In this experiment we observe that the stopping voltage is different for different wavelengths, as expected. With different wavelengths, electrons are expelled with different energies. Increasing the voltage increases the amount of electrons that gain enough energy to be detected, as previously.

== Error analysis <error_analysis>


We would expect all the apertures in the first part (@results_a) to have the same stopping voltage. As seen in @table_a, this was not the case. Since there are three total data points, and two are consistent with theory, we can safely discuss the possibility that the outlier can be dismissed. Most likely this is due to the fact that we recalibrated the instrument after each aperture size adjustment. Another, more plausible suggestion is that we did not let the capacitor finish charging up between measurements. A fully charged capacitor does not have any current of any appreciable size flow through it. If we did not let it charge up between measurements, consistently, our results would be equally skewed. A third, equally plausible explanation would be that some background light in the lab during these measurements excited electrons with higher energies which would account for the higher stopping voltage.

For @results_b we expect different stopping voltages for different frequencies. As discussed in the theory section, a shorter wavelength increases the energy of the photons hitting the plate. Therefore, the excited electrons have more energy than it would for longer wavelengths of light.

Linearization of the graphs are also problematic. Partly due to unexplored errors in the measured parameters, and partly due to the low amount of data points. Finally, the three data points we have for estimating the values of Planck's constant and the work function could definitely be increased. This in turn would yield a result close to the tabulated value. The calculated uncertainties quantify these limitations, allowing us to determine that our results remain statistically compatible with theoretical expectations despite the limited data density.

// for all quantities, use #qty, example: $h = qty("4.707e-34", "J s")$
The aperture series shows weak stopping-voltage dependence and a much stronger slope change. The shared stopping voltage from the three pairwise line intersections is $qty("0.442", "V")$ with a large uncertainty of $qty("0.456", "V")$, which means the data do not resolve a strong aperture effect. That large spread is consistent with cutoff-window sensitivity, calibration drift, and the limited amount of data near the current threshold.

For the wavelength series, the extracted values are $qty("1.172", "V")$, $qty("0.512", "V")$, and $qty("0.117", "V")$ for $qty("365", "nm")$, $qty("405", "nm")$, and $qty("546", "nm")$ respectively. The weighted fit gives $h = qty("4.707e-34", "J s")$ and $W_0 = qty("1.601", "eV")$. Compared with the accepted value $qty("6.62607015e-34", "J s")$, the relative deviation is $qty("29.0", "%")$, but the fitted discrepancy is only $qty("0.67", "sigma")$, so the estimate is still statistically compatible within the current uncertainty model.

The main limitations are the small number of wavelengths and the fact that the stopping voltages are extracted from heuristic linearization windows. A denser wavelength set and a more objective cutoff-selection method would reduce the uncertainty more effectively than simply quoting the current fit result.

It is also worth mentioning that the setup was not as stable as intended. The vacuum lamp and the receiver was much closer than the instructions intended. Therefore small vibrations could've disrupted the measuring process.



#bibliography("references.bib")

