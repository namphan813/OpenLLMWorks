import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  Link,
  useParams,
} from "react-router-dom";

import Layout from "../layout/Layout";


function formatScore(value) {
  if (typeof value !== "number") {
    return "Unknown";
  }

  return value.toFixed(2);
}


function formatVram(hardware) {
  const vram =
    hardware?.gpuIdentity?.vramGib;

  if (typeof vram !== "number") {
    return "Unknown";
  }

  return `${vram} GiB`;
}


function formatMemoryConfigurations(system) {
  const configurations =
    system?.memoryConfigurationsGb;

  if (
    !Array.isArray(configurations) ||
    configurations.length === 0
  ) {
    return "Unknown";
  }

  return configurations
    .map(
      (memory) =>
        `${memory} GB`
    )
    .join(", ");
}


function formatOperatingSystems(system) {
  const operatingSystems =
    system?.operatingSystems;

  if (
    !Array.isArray(operatingSystems) ||
    operatingSystems.length === 0
  ) {
    return "Unknown";
  }

  return operatingSystems.join(", ");
}


function calculateDifference(
  leftValue,
  rightValue,
) {
  if (
    typeof leftValue !== "number" ||
    typeof rightValue !== "number" ||
    leftValue <= 0 ||
    rightValue <= 0
  ) {
    return null;
  }

  if (leftValue === rightValue) {
    return {
      leader: "tie",
      percentage: 0,
    };
  }

  if (leftValue > rightValue) {
    return {
      leader: "left",
      percentage:
        ((leftValue - rightValue) /
          rightValue) *
        100,
    };
  }

  return {
    leader: "right",
    percentage:
      ((rightValue - leftValue) /
        leftValue) *
      100,
  };
}


function getEvidenceLabel(
  submissionCount
) {
  if (
    typeof submissionCount !==
    "number"
  ) {
    return "Unknown sample";
  }

  if (submissionCount <= 1) {
    return "Single result";
  }

  if (submissionCount <= 3) {
    return "Limited sample";
  }

  return "Growing sample";
}


function DifferenceSummary({
  difference,
  leftHardware,
  rightHardware,
}) {
  if (!difference) {
    return (
      <p className="hardware-compare-difference">
        Comparison unavailable
      </p>
    );
  }

  if (
    difference.leader === "tie"
  ) {
    return (
      <p className="hardware-compare-difference">
        Performance is equal
      </p>
    );
  }

  const leader =
    difference.leader === "left"
      ? leftHardware
      : rightHardware;

  return (
    <p className="hardware-compare-difference">
      <strong>
        {leader.gpuModel}
      </strong>
      {" "}
      is
      {" "}
      <strong>
        {difference.percentage.toFixed(
          1
        )}
        %
      </strong>
      {" "}
      faster
    </p>
  );
}


function EvidenceSummary({
  hardware,
}) {
  const submissionCount =
    hardware.submissionCount ?? 0;

  const testedMemoryCount =
    hardware.system
      ?.memoryConfigurationsGb
      ?.length ?? 0;

  const operatingSystemCount =
    hardware.system
      ?.operatingSystems
      ?.length ?? 0;

  return (
    <div className="hardware-compare-evidence">
      <div>
        <span>
          Evidence
        </span>

        <strong>
          {getEvidenceLabel(
            submissionCount
          )}
        </strong>
      </div>

      <div>
        <span>
          Results
        </span>

        <strong>
          {submissionCount}
        </strong>
      </div>

      <div>
        <span>
          Memory configs
        </span>

        <strong>
          {testedMemoryCount}
        </strong>
      </div>

      <div>
        <span>
          OS configs
        </span>

        <strong>
          {operatingSystemCount}
        </strong>
      </div>
    </div>
  );
}


function HardwareCompare() {
  const {
    leftVariantId,
    rightVariantId,
  } = useParams();

  const [
    hardwareData,
    setHardwareData,
  ] = useState(null);

  const [
    error,
    setError,
  ] = useState(null);


  useEffect(() => {
    const hardwareDataUrl =
      `${import.meta.env.BASE_URL}hardware.json`;

    async function loadHardwareData() {
      try {
        const response =
          await fetch(
            hardwareDataUrl
          );

        if (!response.ok) {
          throw new Error(
            `Hardware data request failed: ${response.status}`,
          );
        }

        const data =
          await response.json();

        if (
          !Array.isArray(
            data.hardware
          )
        ) {
          throw new Error(
            "Published hardware data does not contain a hardware list.",
          );
        }

        setHardwareData(data);
      } catch (loadError) {
        console.error(
          "Unable to load hardware comparison data.",
          loadError,
        );

        setError(loadError);
      }
    }

    loadHardwareData();
  }, []);


  const leftHardware =
    useMemo(() => {
      if (!hardwareData) {
        return null;
      }

      return (
        hardwareData.hardware.find(
          (hardware) =>
            hardware.variantId ===
            leftVariantId,
        ) ?? null
      );
    }, [
      hardwareData,
      leftVariantId,
    ]);


  const rightHardware =
    useMemo(() => {
      if (!hardwareData) {
        return null;
      }

      return (
        hardwareData.hardware.find(
          (hardware) =>
            hardware.variantId ===
            rightVariantId,
        ) ?? null
      );
    }, [
      hardwareData,
      rightVariantId,
    ]);


  const sameHardware =
    Boolean(leftHardware) &&
    Boolean(rightHardware) &&
    leftHardware.variantId ===
      rightHardware.variantId;

  const comparisonReady =
    Boolean(leftHardware) &&
    Boolean(rightHardware) &&
    !sameHardware;


  const pp512Difference =
    comparisonReady
      ? calculateDifference(
          leftHardware.performance
            ?.averagePp512,
          rightHardware.performance
            ?.averagePp512,
        )
      : null;


  const tg128Difference =
    comparisonReady
      ? calculateDifference(
          leftHardware.performance
            ?.averageTg128,
          rightHardware.performance
            ?.averageTg128,
        )
      : null;


  return (
    <Layout>
      <section className="hardware-compare-page">
        <div className="hardware-compare-navigation">
          <Link
            className="hardware-back-link"
            to="/hardware"
          >
            ← Back to Hardware
          </Link>

          <Link
            className="hardware-back-link"
            to="/compare"
          >
            Change GPUs
          </Link>
        </div>

        <p className="hardware-profile-eyebrow">
          Hardware Comparison
        </p>

        <h1>
          Compare GPUs
        </h1>

        <p className="hardware-compare-intro">
          Compare published local LLM
          benchmark performance and tested
          configurations side by side.
        </p>

        {error && (
          <div className="hardware-compare-state">
            <p>
              Hardware comparison data
              could not be loaded.
            </p>

            <Link to="/compare">
              Choose GPUs to compare
            </Link>
          </div>
        )}

        {!hardwareData &&
          !error && (
            <p>
              Loading hardware
              comparison...
            </p>
          )}

        {hardwareData &&
          (
            !leftHardware ||
            !rightHardware
          ) && (
            <div className="hardware-compare-state">
              <p>
                One or more requested
                hardware profiles could
                not be found.
              </p>

              <Link to="/compare">
                Choose GPUs to compare
              </Link>
            </div>
          )}

        {hardwareData &&
          sameHardware && (
            <div className="hardware-compare-state">
              <p>
                Choose two different GPUs
                to compare.
              </p>

              <Link to="/compare">
                Choose GPUs to compare
              </Link>
            </div>
          )}

        {comparisonReady && (
          <>
            <div className="hardware-compare-head">
              <article className="hardware-compare-gpu">
                <p className="hardware-profile-eyebrow">
                  {leftHardware.gpuVendor ??
                    "Unknown vendor"}
                </p>

                <h2>
                  {
                    leftHardware.gpuModel
                  }
                </h2>

                <p>
                  {formatVram(
                    leftHardware
                  )}
                  {" · "}
                  {
                    leftHardware.submissionCount
                  }{" "}
                  benchmark result
                  {leftHardware.submissionCount ===
                  1
                    ? ""
                    : "s"}
                </p>

                <EvidenceSummary
                  hardware={
                    leftHardware
                  }
                />
              </article>

              <div className="hardware-compare-vs">
                VS
              </div>

              <article className="hardware-compare-gpu">
                <p className="hardware-profile-eyebrow">
                  {rightHardware.gpuVendor ??
                    "Unknown vendor"}
                </p>

                <h2>
                  {
                    rightHardware.gpuModel
                  }
                </h2>

                <p>
                  {formatVram(
                    rightHardware
                  )}
                  {" · "}
                  {
                    rightHardware.submissionCount
                  }{" "}
                  benchmark result
                  {rightHardware.submissionCount ===
                  1
                    ? ""
                    : "s"}
                </p>

                <EvidenceSummary
                  hardware={
                    rightHardware
                  }
                />
              </article>
            </div>

            <div className="hardware-compare-context">
              <strong>
                Comparison context
              </strong>

              <p>
                Published averages may be
                based on different CPUs,
                memory configurations,
                operating systems, drivers,
                and CUDA environments.
                Results may change as more
                community benchmarks are
                added.
              </p>
            </div>

            <section className="hardware-compare-section">
              <p className="hardware-profile-eyebrow">
                Performance
              </p>

              <h2>
                Prompt Processing
              </h2>

              <p className="hardware-compare-metric-name">
                pp512
              </p>

              <div className="hardware-compare-metrics">
                <article className="hardware-profile-metric">
                  <span>
                    {
                      leftHardware.gpuModel
                    }
                  </span>

                  <strong>
                    {formatScore(
                      leftHardware.performance
                        .averagePp512
                    )}
                  </strong>

                  <span>
                    tokens/sec
                  </span>
                </article>

                <article className="hardware-profile-metric">
                  <span>
                    {
                      rightHardware.gpuModel
                    }
                  </span>

                  <strong>
                    {formatScore(
                      rightHardware.performance
                        .averagePp512
                    )}
                  </strong>

                  <span>
                    tokens/sec
                  </span>
                </article>
              </div>

              <DifferenceSummary
                difference={
                  pp512Difference
                }
                leftHardware={
                  leftHardware
                }
                rightHardware={
                  rightHardware
                }
              />
            </section>

            <section className="hardware-compare-section">
              <h2>
                Token Generation
              </h2>

              <p className="hardware-compare-metric-name">
                tg128
              </p>

              <div className="hardware-compare-metrics">
                <article className="hardware-profile-metric">
                  <span>
                    {
                      leftHardware.gpuModel
                    }
                  </span>

                  <strong>
                    {formatScore(
                      leftHardware.performance
                        .averageTg128
                    )}
                  </strong>

                  <span>
                    tokens/sec
                  </span>
                </article>

                <article className="hardware-profile-metric">
                  <span>
                    {
                      rightHardware.gpuModel
                    }
                  </span>

                  <strong>
                    {formatScore(
                      rightHardware.performance
                        .averageTg128
                    )}
                  </strong>

                  <span>
                    tokens/sec
                  </span>
                </article>
              </div>

              <DifferenceSummary
                difference={
                  tg128Difference
                }
                leftHardware={
                  leftHardware
                }
                rightHardware={
                  rightHardware
                }
              />
            </section>

            <section className="hardware-compare-section">
              <p className="hardware-profile-eyebrow">
                Test Context
              </p>

              <h2>
                Tested Configurations
              </h2>

              <div className="hardware-compare-table">
                <div className="hardware-compare-row hardware-compare-row-head">
                  <div>
                    Configuration
                  </div>

                  <div>
                    {
                      leftHardware.gpuModel
                    }
                  </div>

                  <div>
                    {
                      rightHardware.gpuModel
                    }
                  </div>
                </div>

                <div className="hardware-compare-row">
                  <strong>
                    VRAM
                  </strong>

                  <span>
                    {formatVram(
                      leftHardware
                    )}
                  </span>

                  <span>
                    {formatVram(
                      rightHardware
                    )}
                  </span>
                </div>

                <div className="hardware-compare-row">
                  <strong>
                    Benchmark Results
                  </strong>

                  <span>
                    {
                      leftHardware.submissionCount
                    }
                  </span>

                  <span>
                    {
                      rightHardware.submissionCount
                    }
                  </span>
                </div>

                <div className="hardware-compare-row">
                  <strong>
                    Evidence Level
                  </strong>

                  <span>
                    {getEvidenceLabel(
                      leftHardware.submissionCount
                    )}
                  </span>

                  <span>
                    {getEvidenceLabel(
                      rightHardware.submissionCount
                    )}
                  </span>
                </div>

                <div className="hardware-compare-row">
                  <strong>
                    Tested Memory
                  </strong>

                  <span>
                    {formatMemoryConfigurations(
                      leftHardware.system
                    )}
                  </span>

                  <span>
                    {formatMemoryConfigurations(
                      rightHardware.system
                    )}
                  </span>
                </div>

                <div className="hardware-compare-row">
                  <strong>
                    Operating Systems
                  </strong>

                  <span>
                    {formatOperatingSystems(
                      leftHardware.system
                    )}
                  </span>

                  <span>
                    {formatOperatingSystems(
                      rightHardware.system
                    )}
                  </span>
                </div>
              </div>
            </section>

            <div className="hardware-compare-actions">
              <Link
                to={`/hardware/${leftHardware.variantId}`}
              >
                View{" "}
                {
                  leftHardware.gpuModel
                }
              </Link>

              <Link
                to={`/hardware/${rightHardware.variantId}`}
              >
                View{" "}
                {
                  rightHardware.gpuModel
                }
              </Link>
            </div>

            <p className="hardware-compare-note">
              Performance differences
              describe the currently
              published averages, not a
              controlled head-to-head test.
              Sample counts and tested
              environments may differ.
            </p>
          </>
        )}
      </section>
    </Layout>
  );
}


export default HardwareCompare;