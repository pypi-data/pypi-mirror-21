/*
 * dna-traits
 * Copyright 2014, 2016 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 *
 * arv
 * Copyright 2017 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 */

#ifndef ARV_ARV_HPP
#define ARV_ARV_HPP

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace arv {

typedef std::uint32_t Position;
typedef std::int32_t RSID;

enum Nucleotide {
  NONE, A, G, C, T, D, I
};

enum Chromosome {
  CHR_NO =  0,
  CHR_01 =  1,
  CHR_02 =  2,
  CHR_03 =  3,
  CHR_04 =  4,
  CHR_05 =  5,
  CHR_06 =  6,
  CHR_07 =  7,
  CHR_08 =  8,
  CHR_09 =  9,
  CHR_10 = 10,
  CHR_11 = 11,
  CHR_12 = 12,
  CHR_13 = 13,
  CHR_14 = 14,
  CHR_15 = 15,
  CHR_16 = 16,
  CHR_17 = 17,
  CHR_18 = 18,
  CHR_19 = 19,
  CHR_20 = 20,
  CHR_21 = 21,
  CHR_22 = 22,
  CHR_X  = 23,
  CHR_Y  = 24,
  CHR_MT = 25 // Mitochondrial DNA
};

// We can get this down to a byte if we want to
#pragma pack(1)
struct Genotype {
  Nucleotide first  : 3;
  Nucleotide second : 3;

  Genotype();
  Genotype(const Nucleotide& a, const Nucleotide& b);

  friend Genotype operator~(const Genotype&);
  bool operator==(const Genotype& g) const;
  bool operator<(const Genotype& g) const;

  std::string to_string() const;
};

#pragma pack(1)
struct SNP {
  Chromosome chromosome : 5;
  Position position;
  Genotype genotype;

  SNP();
  SNP(const Chromosome&, const Position&, const Genotype&);
  SNP(const SNP&);
  SNP& operator=(const SNP&);

  // Comparisons are based on the tuple (position, chromosome, genotype)
  bool operator!=(const SNP&) const;
  bool operator<(const SNP&) const;
  bool operator<=(const SNP&) const;
  bool operator==(const Genotype&) const;
  bool operator==(const SNP&) const;
  bool operator>(const SNP&) const;
  bool operator>=(const SNP&) const;
};

extern const SNP NONE_SNP;

struct GenomeIteratorImpl;

typedef std::pair<RSID, SNP> RsidSNP;

struct GenomeIterator {
  GenomeIterator();
  GenomeIterator(const GenomeIterator&);
  GenomeIterator(GenomeIteratorImpl*);
  GenomeIterator& operator=(const GenomeIterator&);
  ~GenomeIterator();

  bool operator==(const GenomeIterator&) const;
  bool operator!=(const GenomeIterator&) const;

  void next();
  RsidSNP value() const;

private:
  GenomeIteratorImpl* pimpl;
};

struct Genome {
  /*!
   * True if genome contains a Y-chromosome (with non-empty genotypes).
   */
  bool y_chromosome;

  Genome();
  Genome(const std::size_t size);
  Genome(const Genome&);
  Genome& operator=(const Genome&);
  ~Genome();

  /*!
   * Access SNP. Throws on not found.
   */
  const SNP& operator[](const RSID& id) const;

  /*!
   * Checks if hash table contains given RSID.
   */
  bool has(const RSID& id) const;

  /*!
   * Add a SNP to the hash table.
   */
  void insert(const RsidSNP&);

  /*!
   * Underlying hash table's load factor. (For developer purposes)
   */
  double load_factor() const;

  /*!
   * Number of SNPs.
   */
  std::size_t size() const;

  bool operator==(const Genome&) const;
  bool operator!=(const Genome&) const;

  GenomeIterator begin() const;
  GenomeIterator end() const;

private:
  struct GenomeImpl;
  GenomeImpl* pimpl;
};

Nucleotide complement(const Nucleotide& n);

/*!
 * Parse a 23andMe genome text file and put contents into genome.
 */
void parse_file(const std::string& filename, Genome&);

Genotype complement(const Genotype& g);

} // namespace arv

#endif // include guard
