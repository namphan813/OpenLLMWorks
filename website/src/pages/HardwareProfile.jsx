import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import Layout from "../layout/Layout";

function formatScore(value) {
  if (typeof value !== "number") {
    return "Unknown";
  }

  return value.toFixed(2);
}

function formatMemoryConfigurations(system) {
  const configurations = system?.memoryConfigurationsGb;

  if (
    Array.isArray(configurations) &&
    configurations.length > 0
  ) {
    return configurations
      .map((memory) => `${memory} GB`)
      .join(", ");
  }

  return "Unknown";
}

function HardwareProfile() {
  const { variantId: requestedVariantId } = useParams();

  const [hardware, setHardware] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const hardwareDataUrl =
      `${import.meta.env.BASE_URL}hardware.json`;

    async function loadHardwareProfile() {
      try {
        const response = await fetch(hardwareDataUrl);

        if (!response.ok) {
          throw new Error(
            `Hardware data request failed: ${response.status}`,
          );
        }

        const data = await response.json();

        if (!Array.isArray(data.hardware)) {
          throw new Error(
            "Published hardware data does not contain a hardware list.",
          );
        }

        const matchedHardware = data.hardware.find(
          (item) => item.variantId === requestedVariantId,
        );

        if (!matchedHardware) {
          throw new Error("Hardware profile not found.");
        }

        setHardware(matchedHardware);
      } catch (loadError) {
        console.error(
          "Unable to load hardware profile.",
          loadError,
        );

        setError(loadError);
      }
    }

    loadHardwareProfile();
  }, [requestedVariantId]);

  return (
    <Layout>
      <section className="hardware-profile-page">
        <Link
          to="/hardware"
          className="hardware-back-link"
        >
          ← Back to Hardware
        </Link>

        {error && (
          <p>
            Hardware profile could not be loaded.
          </p>
        )}

        {!hardware && !error && (
          <p>
            Loading hardware profile...
          </p>
        )}

        {hardware && (
          <>
            <p className="hardware-profile-eyebrow">
              {hardware.gpuVendor ?? "Hardware Profile"}
            </p>

            <h1>{hardware.gpuModel}</h1>

            <p>
              {hardware.gpuIdentity?.vramGib ?? "Unknown"}{" "}
              GiB VRAM
              {" · "}
              {hardware.submissionCount} benchmark result
              {hardware.submissionCount === 1 ? "" : "s"}
            </p>

            <div className="hardware-profile-metrics">
              <article className="hardware-profile-metric">
                <span>Average pp512</span>

                <strong>
                  {formatScore(
                    hardware.performance.averagePp512,
                  )}
                </strong>

                <span>tokens/sec</span>
              </article>

              <article className="hardware-profile-metric">
                <span>Average tg128</span>

                <strong>
                  {formatScore(
                    hardware.performance.averageTg128,
                  )}
                </strong>

                <span>tokens/sec</span>
              </article>
            </div>

            <div className="hardware-profile-details">
              <h2>Performance</h2>

              <p>
                Best pp512:{" "}
                <strong>
                  {formatScore(
                    hardware.performance.bestPp512,
                  )}
                </strong>
              </p>

              <p>
                Worst pp512:{" "}
                <strong>
                  {formatScore(
                    hardware.performance.worstPp512,
                  )}
                </strong>
              </p>

              <h2>Tested Configurations</h2>

              <p>
                Tested Memory:{" "}
                <strong>
                  {formatMemoryConfigurations(
                    hardware.system,
                  )}
                </strong>
              </p>

              <p>
                Operating Systems:{" "}
                <strong>
                  {hardware.system.operatingSystems.length > 0
                    ? hardware.system.operatingSystems.join(", ")
                    : "Unknown"}
                </strong>
              </p>
            </div>

            <section className="hardware-benchmark-results">
              <div className="hardware-benchmark-results-header">
                <div>
                  <p className="hardware-profile-eyebrow">
                    Benchmark History
                  </p>

                  <h2>Benchmark Results</h2>
                </div>

                <p>
                  {hardware.benchmarkResults?.length ?? 0} recorded
                </p>
              </div>

              {hardware.benchmarkResults?.length > 0 ? (
                <div className="hardware-benchmark-list">
                  {hardware.benchmarkResults.map(
                    (result, index) => (
                      <article
                        className="hardware-benchmark-result"
                        key={`${result.submissionName}-${index}`}
                      >
                        <div className="hardware-benchmark-title">
                          <div>
                            <h3>
                              {result.submissionName ?? "Unknown submission"}
                            </h3>

                            <p className="hardware-benchmark-cpu">
                              {result.cpuModel ?? "Unknown CPU"}
                            </p>
                          </div>

                          <span>
                            {result.operatingSystem ?? "Unknown OS"}
                          </span>
                        </div>

                        <div className="hardware-benchmark-grid">
                          <div>
                            <span>pp512</span>

                            <strong>
                              {formatScore(result.pp512)}
                            </strong>

                            <small>tokens/sec</small>
                          </div>

                          <div>
                            <span>tg128</span>

                            <strong>
                              {formatScore(result.tg128)}
                            </strong>

                            <small>tokens/sec</small>
                          </div>

                          <div>
                            <span>System Memory</span>

                            <strong>
                              {result.memoryGb ?? "Unknown"}
                            </strong>

                            <small>GB</small>
                          </div>

                          <div>
                            <span>VRAM</span>

                            <strong>
                              {result.vramGib ?? "Unknown"}
                            </strong>

                            <small>GiB</small>
                          </div>
                        </div>
                      </article>
                    ),
                  )}
                </div>
              ) : (
                <p>
                  No individual benchmark results are available.
                </p>
              )}
            </section>
          </>
        )}
      </section>
    </Layout>
  );
}

export default HardwareProfile;