import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  Link,
  useNavigate,
  useSearchParams,
} from "react-router-dom";

import Layout from "../layout/Layout";


function formatScore(value) {
  if (typeof value !== "number") {
    return "Unknown";
  }

  return value.toFixed(2);
}


function formatMemoryConfigurations(system) {
  const configurations =
    system?.memoryConfigurationsGb;

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


function compareByGpuName(
  left,
  right
) {
  return left.gpuModel.localeCompare(
    right.gpuModel
  );
}


function compareDescendingWithNameTieBreak(
  leftValue,
  rightValue,
  leftHardware,
  rightHardware
) {
  const normalizedLeft =
    typeof leftValue === "number"
      ? leftValue
      : -Infinity;

  const normalizedRight =
    typeof rightValue === "number"
      ? rightValue
      : -Infinity;

  const metricDifference =
    normalizedRight -
    normalizedLeft;

  if (metricDifference !== 0) {
    return metricDifference;
  }

  return compareByGpuName(
    leftHardware,
    rightHardware
  );
}


function Hardware() {
  const navigate = useNavigate();

  const [searchParams] =
    useSearchParams();

  const requestedCompareVariantId =
    searchParams.get("compare");

  const [
    hardwareData,
    setHardwareData,
  ] = useState(null);

  const [
    error,
    setError,
  ] = useState(null);

  const [
    searchQuery,
    setSearchQuery,
  ] = useState("");

  const [
    vendorFilter,
    setVendorFilter,
  ] = useState("all");

  const [
    vramFilter,
    setVramFilter,
  ] = useState("all");

  const [
    sortBy,
    setSortBy,
  ] = useState("name");

  const [
    compareSelection,
    setCompareSelection,
  ] = useState(null);


  useEffect(() => {
    const hardwareDataUrl =
      `${import.meta.env.BASE_URL}hardware.json`;

    async function loadHardwareData() {
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

        setHardwareData(data);
      } catch (loadError) {
        console.error(
          "Unable to load published hardware data.",
          loadError,
        );

        setError(loadError);
      }
    }

    loadHardwareData();
  }, []);


  useEffect(() => {
    if (
      !hardwareData ||
      !requestedCompareVariantId
    ) {
      return;
    }

    const requestedHardware =
      hardwareData.hardware.find(
        (hardware) =>
          hardware.variantId ===
          requestedCompareVariantId
      );

    if (!requestedHardware) {
      return;
    }

    setCompareSelection(
      requestedHardware
    );
  }, [
    hardwareData,
    requestedCompareVariantId,
  ]);


  const availableVendors =
    useMemo(() => {
      if (!hardwareData) {
        return [];
      }

      return [
        ...new Set(
          hardwareData.hardware
            .map(
              (hardware) =>
                hardware.gpuVendor
            )
            .filter(
              (vendor) =>
                vendor &&
                vendor !==
                  "Unknown"
            )
        ),
      ].sort((left, right) =>
        left.localeCompare(right)
      );
    }, [hardwareData]);


  const pp512Ranking =
    useMemo(() => {
      if (!hardwareData) {
        return {
          totalRanked: 0,
          bestValue: null,
          rankByVariantId:
            new Map(),
        };
      }

      return buildMetricRanking(
        hardwareData.hardware,
        (hardware) =>
          hardware.performance
            ?.averagePp512
      );
    }, [hardwareData]);


  const tg128Ranking =
    useMemo(() => {
      if (!hardwareData) {
        return {
          totalRanked: 0,
          bestValue: null,
          rankByVariantId:
            new Map(),
        };
      }

      return buildMetricRanking(
        hardwareData.hardware,
        (hardware) =>
          hardware.performance
            ?.averageTg128
      );
    }, [hardwareData]);


  const visibleHardware =
    useMemo(() => {
      if (!hardwareData) {
        return [];
      }

      const normalizedSearch =
        searchQuery
          .trim()
          .toLowerCase();

      const filtered =
        hardwareData.hardware.filter(
          (hardware) => {
            const matchesVendor =
              vendorFilter === "all" ||
              hardware.gpuVendor ===
                vendorFilter;

            if (!matchesVendor) {
              return false;
            }

            const vram =
              hardware.gpuIdentity
                ?.vramGib;

            const matchesVram =
              vramFilter === "all" ||
              (
                typeof vram ===
                  "number" &&
                vram >=
                  Number(vramFilter)
              );

            if (!matchesVram) {
              return false;
            }

            if (!normalizedSearch) {
              return true;
            }

            const searchableValues = [
              hardware.gpuVendor,
              hardware.gpuModel,
              hardware.gpuIdentity
                ?.vramGib,
              hardware.gpuIdentity
                ?.formFactor,
              hardware.performance
                ?.averagePp512,
              hardware.performance
                ?.averageTg128,
              hardware.system
                ?.averageMemoryGb,
              ...(
                hardware.system
                  ?.memoryConfigurationsGb ??
                []
              ),
              ...(
                hardware.system
                  ?.operatingSystems ??
                []
              ),
            ];

            return searchableValues.some(
              (value) =>
                String(
                  value ?? ""
                )
                  .toLowerCase()
                  .includes(
                    normalizedSearch
                  )
            );
          }
        );

      return [...filtered].sort(
        (left, right) => {
          if (sortBy === "vram") {
            return compareDescendingWithNameTieBreak(
              left.gpuIdentity
                ?.vramGib,
              right.gpuIdentity
                ?.vramGib,
              left,
              right
            );
          }

          if (sortBy === "pp512") {
            return compareDescendingWithNameTieBreak(
              left.performance
                ?.averagePp512,
              right.performance
                ?.averagePp512,
              left,
              right
            );
          }

          if (sortBy === "tg128") {
            return compareDescendingWithNameTieBreak(
              left.performance
                ?.averageTg128,
              right.performance
                ?.averageTg128,
              left,
              right
            );
          }

          if (
            sortBy ===
            "benchmarks"
          ) {
            return compareDescendingWithNameTieBreak(
              left.submissionCount,
              right.submissionCount,
              left,
              right
            );
          }

          return compareByGpuName(
            left,
            right
          );
        }
      );
    }, [
      hardwareData,
      searchQuery,
      vendorFilter,
      vramFilter,
      sortBy,
    ]);


  function handleCompare(
    hardware
  ) {
    if (!compareSelection) {
      setCompareSelection(
        hardware
      );

      return;
    }

    if (
      compareSelection.variantId ===
      hardware.variantId
    ) {
      setCompareSelection(null);

      return;
    }

    navigate(
      `/compare/${compareSelection.variantId}/${hardware.variantId}`
    );
  }


  function cancelComparison() {
    setCompareSelection(null);
  }


  return (
    <Layout>
      <section className="hardware-page">
        <h1>Hardware</h1>

        <p>
          Explore local LLM benchmark
          performance across
          community-tested hardware.
        </p>

        {error && (
          <p>
            Hardware data could not be
            loaded.
          </p>
        )}

        {!hardwareData &&
          !error && (
            <p>
              Loading hardware data...
            </p>
          )}

        {hardwareData && (
          <>
            <div className="hardware-summary-row">
              <p>
                {
                  hardwareData.summary
                    .gpuVariants
                }{" "}
                GPU variants
                {" · "}
                {
                  hardwareData.summary
                    .benchmarkResults
                }{" "}
                benchmark results
              </p>

              <Link
                to="/compare"
                className="hardware-compare-link"
              >
                Compare GPUs →
              </Link>
            </div>

            {compareSelection && (
              <div className="hardware-compare-selection">
                <div>
                  <span>
                    Comparing:
                  </span>

                  <strong>
                    {
                      compareSelection.gpuModel
                    }
                  </strong>

                  <small>
                    Choose another GPU
                    below to compare.
                  </small>
                </div>

                <button
                  type="button"
                  onClick={
                    cancelComparison
                  }
                >
                  Cancel comparison
                </button>
              </div>
            )}

            <div className="hardware-controls">
              <label className="hardware-search">
                <span>
                  Search hardware
                </span>

                <input
                  type="search"
                  value={searchQuery}
                  onChange={(event) =>
                    setSearchQuery(
                      event.target.value
                    )
                  }
                  placeholder="Search GPU, vendor, score, VRAM, OS..."
                />
              </label>

              <div className="hardware-filter-group">
                <label className="hardware-vendor-filter">
                  <span>
                    Vendor
                  </span>

                  <select
                    value={
                      vendorFilter
                    }
                    onChange={(event) =>
                      setVendorFilter(
                        event.target
                          .value
                      )
                    }
                  >
                    <option value="all">
                      All vendors
                    </option>

                    {availableVendors.map(
                      (vendor) => (
                        <option
                          key={vendor}
                          value={vendor}
                        >
                          {vendor}
                        </option>
                      )
                    )}
                  </select>
                </label>

                <label className="hardware-vram-filter">
                  <span>
                    VRAM
                  </span>

                  <select
                    value={
                      vramFilter
                    }
                    onChange={(event) =>
                      setVramFilter(
                        event.target
                          .value
                      )
                    }
                  >
                    <option value="all">
                      All VRAM
                    </option>

                    <option value="4">
                      4 GiB+
                    </option>

                    <option value="6">
                      6 GiB+
                    </option>

                    <option value="8">
                      8 GiB+
                    </option>

                    <option value="12">
                      12 GiB+
                    </option>

                    <option value="16">
                      16 GiB+
                    </option>
                  </select>
                </label>

                <label className="hardware-sort">
                  <span>
                    Sort by
                  </span>

                  <select
                    value={sortBy}
                    onChange={(event) =>
                      setSortBy(
                        event.target.value
                      )
                    }
                  >
                    <option value="name">
                      GPU name
                    </option>

                    <option value="pp512">
                      pp512 — fastest
                    </option>

                    <option value="tg128">
                      tg128 — fastest
                    </option>

                    <option value="vram">
                      VRAM — highest
                    </option>

                    <option value="benchmarks">
                      Most benchmarked
                    </option>
                  </select>
                </label>
              </div>
            </div>

            <p className="hardware-result-count">
              Showing{" "}
              {
                visibleHardware.length
              }{" "}
              of{" "}
              {
                hardwareData.hardware
                  .length
              }{" "}
              GPU variants
            </p>

            {visibleHardware.length >
            0 ? (
              <div className="hardware-list">
                {visibleHardware.map(
                  (hardware) => {
                    const isSelected =
                      compareSelection
                        ?.variantId ===
                      hardware.variantId;

                    const pp512 =
                      hardware.performance
                        ?.averagePp512;

                    const tg128 =
                      hardware.performance
                        ?.averageTg128;

                    const pp512Rank =
                      pp512Ranking.rankByVariantId.get(
                        hardware.variantId
                      );

                    const tg128Rank =
                      tg128Ranking.rankByVariantId.get(
                        hardware.variantId
                      );

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

                    return (
                      <article
                        className={`hardware-card ${
                          isSelected
                            ? "hardware-card-selected"
                            : ""
                        }`}
                        key={
                          hardware.variantId
                        }
                      >
                        <p className="hardware-card-vendor">
                          {hardware.gpuVendor ??
                            "Unknown vendor"}
                        </p>

                        <h2>
                          {
                            hardware.gpuModel
                          }
                        </h2>

                        <p>
                          Benchmarks:{" "}
                          {
                            hardware.submissionCount
                          }
                        </p>

                        <p>
                          VRAM:
                          {" "}
                          {hardware.gpuIdentity
                            ?.vramGib ??
                            "Unknown"}{" "}
                          GiB
                        </p>

                        <p>
                          Tested Memory:
                          {" "}
                          {formatMemoryConfigurations(
                            hardware.system
                          )}
                        </p>

                        <div className="hardware-card-performance">
                          <div className="hardware-card-performance-header">
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
                            {" "}
                            <small>
                              tokens/sec
                            </small>
                          </strong>

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
                        </div>

                        <div className="hardware-card-performance">
                          <div className="hardware-card-performance-header">
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
                            {" "}
                            <small>
                              tokens/sec
                            </small>
                          </strong>

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
                        </div>

                        <p>
                          Operating Systems:
                          {" "}
                          {hardware.system
                            ?.operatingSystems
                            ?.length > 0
                            ? hardware.system.operatingSystems.join(
                                ", "
                              )
                            : "Unknown"}
                        </p>

                        <div className="hardware-card-actions">
                          <Link
                            to={`/hardware/${hardware.variantId}`}
                          >
                            View Profile
                          </Link>

                          <button
                            type="button"
                            className={
                              isSelected
                                ? "hardware-compare-button-selected"
                                : ""
                            }
                            onClick={() =>
                              handleCompare(
                                hardware
                              )
                            }
                          >
                            {isSelected
                              ? "Selected"
                              : compareSelection
                                ? "Compare with this GPU"
                                : "Compare"}
                          </button>
                        </div>
                      </article>
                    );
                  }
                )}
              </div>
            ) : (
              <p className="hardware-empty">
                No hardware matches the
                current filters.
              </p>
            )}
          </>
        )}
      </section>
    </Layout>
  );
}


export default Hardware;