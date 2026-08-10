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


function formatSoftwareValue(value) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return "Unknown";
  }

  return value;
}


function buildMetricRanking(
  hardwareList,
  metricSelector
) {
  const ranked = hardwareList
    .map((hardware) => ({
      variantId: hardware.variantId,
      value: metricSelector(hardware),
    }))
    .filter(
      (item) =>
        typeof item.value === "number"
    )
    .sort(
      (left, right) =>
        right.value - left.value
    );

  const rankByVariantId =
    new Map();

  ranked.forEach(
    (item, index) => {
      rankByVariantId.set(
        item.variantId,
        index + 1
      );
    }
  );

  return {
    totalRanked: ranked.length,
    bestValue:
      ranked.length > 0
        ? ranked[0].value
        : null,
    rankByVariantId,
  };
}


function calculateBarWidth(
  value,
  bestValue
) {
  if (
    typeof value !== "number" ||
    typeof bestValue !== "number" ||
    bestValue <= 0
  ) {
    return 0;
  }

  return Math.max(
    0,
    Math.min(
      100,
      (value / bestValue) * 100
    )
  );
}


function HardwareProfile() {
  const {
    variantId: requestedVariantId,
  } = useParams();

  const [
    hardware,
    setHardware,
  ] = useState(null);

  const [
    hardwareList,
    setHardwareList,
  ] = useState([]);

  const [
    error,
    setError,
  ] = useState(null);

  const [
    activeFilter,
    setActiveFilter,
  ] = useState({
    type: "all",
    value: null,
  });


  useEffect(() => {
    const hardwareDataUrl =
      `${import.meta.env.BASE_URL}hardware.json`;

    async function loadHardwareProfile() {
      try {
        const response = await fetch(
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

        const matchedHardware =
          data.hardware.find(
            (item) =>
              item.variantId ===
              requestedVariantId
          );

        if (!matchedHardware) {
          throw new Error(
            "Hardware profile not found."
          );
        }

        setHardwareList(
          data.hardware
        );

        setHardware(
          matchedHardware
        );

        setActiveFilter({
          type: "all",
          value: null,
        });
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


  const pp512Ranking =
    useMemo(() => {
      return buildMetricRanking(
        hardwareList,
        (item) =>
          item.performance
            ?.averagePp512
      );
    }, [hardwareList]);


  const tg128Ranking =
    useMemo(() => {
      return buildMetricRanking(
        hardwareList,
        (item) =>
          item.performance
            ?.averageTg128
      );
    }, [hardwareList]);


  const pp512 =
    hardware?.performance
      ?.averagePp512;

  const tg128 =
    hardware?.performance
      ?.averageTg128;


  const pp512Rank =
    hardware
      ? pp512Ranking
          .rankByVariantId
          .get(
            hardware.variantId
          )
      : null;

  const tg128Rank =
    hardware
      ? tg128Ranking
          .rankByVariantId
          .get(
            hardware.variantId
          )
      : null;


  const pp512BarWidth =
    calculateBarWidth(
      pp512,
      pp512Ranking.bestValue
    );

  const tg128BarWidth =
    calculateBarWidth(
      tg128,
      tg128Ranking.bestValue
    );


  const memoryConfigurations =
    useMemo(() => {
      if (!hardware) {
        return [];
      }

      return [
        ...new Set(
          (
            hardware.benchmarkResults ??
            []
          )
            .map(
              (result) =>
                result.memoryGb
            )
            .filter(
              (memory) =>
                typeof memory ===
                "number"
            )
        ),
      ].sort(
        (left, right) =>
          left - right
      );
    }, [hardware]);


  const operatingSystems =
    useMemo(() => {
      if (!hardware) {
        return [];
      }

      return [
        ...new Set(
          (
            hardware.benchmarkResults ??
            []
          )
            .map(
              (result) =>
                result.operatingSystem
            )
            .filter(
              (operatingSystem) =>
                operatingSystem &&
                operatingSystem !==
                  "Unknown"
            )
        ),
      ].sort(
        (left, right) =>
          left.localeCompare(
            right
          )
      );
    }, [hardware]);


  const visibleResults =
    useMemo(() => {
      const results =
        hardware?.benchmarkResults ??
        [];

      if (
        activeFilter.type ===
        "all"
      ) {
        return results;
      }

      if (
        activeFilter.type ===
        "memory"
      ) {
        return results.filter(
          (result) =>
            result.memoryGb ===
            activeFilter.value
        );
      }

      if (
        activeFilter.type ===
        "os"
      ) {
        return results.filter(
          (result) =>
            result.operatingSystem ===
            activeFilter.value
        );
      }

      if (
        activeFilter.type ===
        "best-pp512"
      ) {
        const bestPp512 =
          hardware?.performance
            ?.bestPp512;

        return results.filter(
          (result) =>
            result.pp512 ===
            bestPp512
        );
      }

      if (
        activeFilter.type ===
        "worst-pp512"
      ) {
        const worstPp512 =
          hardware?.performance
            ?.worstPp512;

        return results.filter(
          (result) =>
            result.pp512 ===
            worstPp512
        );
      }

      return results;
    }, [
      hardware,
      activeFilter,
    ]);


  function setFilter(
    type,
    value = null
  ) {
    setActiveFilter({
      type,
      value,
    });
  }


  function isActiveFilter(
    type,
    value = null
  ) {
    return (
      activeFilter.type === type &&
      activeFilter.value === value
    );
  }


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
            Hardware profile could not
            be loaded.
          </p>
        )}

        {!hardware &&
          !error && (
            <p>
              Loading hardware profile...
            </p>
          )}

        {hardware && (
          <>
            <p className="hardware-profile-eyebrow">
              {hardware.gpuVendor ??
                "Hardware Profile"}
            </p>

            <h1>
              {hardware.gpuModel}
            </h1>

            <p>
              {hardware.gpuIdentity
                ?.vramGib ??
                "Unknown"}{" "}
              GiB VRAM
              {" · "}
              {
                hardware.submissionCount
              }{" "}
              benchmark result
              {hardware.submissionCount ===
              1
                ? ""
                : "s"}
            </p>

            <div className="hardware-profile-actions">
              <Link
                to={`/hardware?compare=${hardware.variantId}`}
                className="hardware-profile-compare-link"
              >
                Compare this GPU →
              </Link>
            </div>

            <div className="hardware-profile-metrics">
              <article className="hardware-profile-metric">
                <div className="hardware-profile-metric-header">
                  <span>
                    Average pp512
                  </span>

                  {pp512Rank && (
                    <small>
                      #{pp512Rank} of{" "}
                      {
                        pp512Ranking.totalRanked
                      }
                    </small>
                  )}
                </div>

                <strong>
                  {formatScore(
                    pp512
                  )}
                </strong>

                <span>
                  tokens/sec
                </span>

                <div
                  className="hardware-performance-track"
                  aria-hidden="true"
                >
                  <span
                    style={{
                      width:
                        `${pp512BarWidth}%`,
                    }}
                  />
                </div>
              </article>

              <article className="hardware-profile-metric">
                <div className="hardware-profile-metric-header">
                  <span>
                    Average tg128
                  </span>

                  {tg128Rank && (
                    <small>
                      #{tg128Rank} of{" "}
                      {
                        tg128Ranking.totalRanked
                      }
                    </small>
                  )}
                </div>

                <strong>
                  {formatScore(
                    tg128
                  )}
                </strong>

                <span>
                  tokens/sec
                </span>

                <div
                  className="hardware-performance-track"
                  aria-hidden="true"
                >
                  <span
                    style={{
                      width:
                        `${tg128BarWidth}%`,
                    }}
                  />
                </div>
              </article>
            </div>

            <div className="hardware-profile-details">
              <h2>
                Performance
              </h2>

              <p>
                Best pp512:{" "}
                <button
                  type="button"
                  className={`hardware-filter-chip ${
                    isActiveFilter(
                      "best-pp512"
                    )
                      ? "hardware-filter-chip-active"
                      : ""
                  }`}
                  onClick={() =>
                    setFilter(
                      "best-pp512"
                    )
                  }
                >
                  {formatScore(
                    hardware.performance
                      ?.bestPp512
                  )}
                </button>
              </p>

              <p>
                Worst pp512:{" "}
                <button
                  type="button"
                  className={`hardware-filter-chip ${
                    isActiveFilter(
                      "worst-pp512"
                    )
                      ? "hardware-filter-chip-active"
                      : ""
                  }`}
                  onClick={() =>
                    setFilter(
                      "worst-pp512"
                    )
                  }
                >
                  {formatScore(
                    hardware.performance
                      ?.worstPp512
                  )}
                </button>
              </p>

              <h2>
                Tested Configurations
              </h2>

              <div className="hardware-filter-row">
                <span>
                  Tested Memory:
                </span>

                <div className="hardware-filter-chips">
                  <button
                    type="button"
                    className={`hardware-filter-chip ${
                      isActiveFilter(
                        "all"
                      )
                        ? "hardware-filter-chip-active"
                        : ""
                    }`}
                    onClick={() =>
                      setFilter("all")
                    }
                  >
                    All
                  </button>

                  {memoryConfigurations.map(
                    (memory) => (
                      <button
                        type="button"
                        key={memory}
                        className={`hardware-filter-chip ${
                          isActiveFilter(
                            "memory",
                            memory
                          )
                            ? "hardware-filter-chip-active"
                            : ""
                        }`}
                        onClick={() =>
                          setFilter(
                            "memory",
                            memory
                          )
                        }
                      >
                        {memory} GB
                      </button>
                    )
                  )}
                </div>
              </div>

              <div className="hardware-filter-row">
                <span>
                  Operating Systems:
                </span>

                <div className="hardware-filter-chips">
                  {operatingSystems.map(
                    (
                      operatingSystem
                    ) => (
                      <button
                        type="button"
                        key={
                          operatingSystem
                        }
                        className={`hardware-filter-chip ${
                          isActiveFilter(
                            "os",
                            operatingSystem
                          )
                            ? "hardware-filter-chip-active"
                            : ""
                        }`}
                        onClick={() =>
                          setFilter(
                            "os",
                            operatingSystem
                          )
                        }
                      >
                        {
                          operatingSystem
                        }
                      </button>
                    )
                  )}
                </div>
              </div>
            </div>

            <section className="hardware-benchmark-results">
              <div className="hardware-benchmark-results-header">
                <div>
                  <p className="hardware-profile-eyebrow">
                    Benchmark History
                  </p>

                  <h2>
                    Benchmark Results
                  </h2>
                </div>

                <div>
                  <p>
                    Showing{" "}
                    {
                      visibleResults.length
                    }{" "}
                    of{" "}
                    {hardware
                      .benchmarkResults
                      ?.length ?? 0}
                  </p>

                  {activeFilter.type !==
                    "all" && (
                    <button
                      type="button"
                      className="hardware-clear-filter"
                      onClick={() =>
                        setFilter(
                          "all"
                        )
                      }
                    >
                      Clear filter
                    </button>
                  )}
                </div>
              </div>

              {visibleResults.length >
              0 ? (
                <div className="hardware-benchmark-list">
                  {visibleResults.map(
                    (
                      result,
                      index
                    ) => (
                      <article
                        className="hardware-benchmark-result"
                        key={`${result.submissionName}-${index}`}
                      >
                        <div className="hardware-benchmark-title">
                          <div>
                            <h3>
                              {result.submissionName ??
                                "Unknown submission"}
                            </h3>

                            <p className="hardware-benchmark-cpu">
                              {result.cpuModel ??
                                "Unknown CPU"}
                            </p>
                          </div>

                          <span>
                            {result.operatingSystem ??
                              "Unknown OS"}
                          </span>
                        </div>

                        <div className="hardware-benchmark-grid">
                          <div>
                            <span>
                              pp512
                            </span>

                            <strong>
                              {formatScore(
                                result.pp512
                              )}
                            </strong>

                            <small>
                              tokens/sec
                            </small>
                          </div>

                          <div>
                            <span>
                              tg128
                            </span>

                            <strong>
                              {formatScore(
                                result.tg128
                              )}
                            </strong>

                            <small>
                              tokens/sec
                            </small>
                          </div>

                          <div>
                            <span>
                              System Memory
                            </span>

                            <strong>
                              {result.memoryGb ??
                                "Unknown"}
                            </strong>

                            <small>
                              GB
                            </small>
                          </div>

                          <div>
                            <span>
                              VRAM
                            </span>

                            <strong>
                              {result.vramGib ??
                                "Unknown"}
                            </strong>

                            <small>
                              GiB
                            </small>
                          </div>
                        </div>

                        <div className="hardware-benchmark-software">
                          <span>
                            Driver{" "}
                            <strong>
                              {formatSoftwareValue(
                                result.driverVersion
                              )}
                            </strong>
                          </span>

                          <span>
                            CUDA{" "}
                            <strong>
                              {formatSoftwareValue(
                                result.cudaUmdVersion
                              )}
                            </strong>
                          </span>
                        </div>
                      </article>
                    )
                  )}
                </div>
              ) : (
                <p>
                  No benchmark results
                  match the current filter.
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