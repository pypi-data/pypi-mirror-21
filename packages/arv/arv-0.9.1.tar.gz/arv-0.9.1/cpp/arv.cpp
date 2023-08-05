/*
 * dna-traits
 * Copyright 2014, 2016, 2017 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 *
 * arv
 * Copyright 2017 Christian Stigen Larsen
 * Distributed under the GNU GPL v3 or later. See COPYING.
 */

#include <google/dense_hash_map>

#include "arv.hpp"

namespace {

struct RSIDHash {
  inline std::size_t operator() (const arv::RSID& rsid) const
  {
    return static_cast<std::size_t>(rsid);
  }
};

struct RSIDEq {
  inline bool operator()(const arv::RSID& a, const arv::RSID& b) const
  {
    return a == b;
  }
};

typedef google::dense_hash_map<arv::RSID, arv::SNP, RSIDHash, RSIDEq> SNPMap;

} // anonymus namespace

namespace arv {

const SNP NONE_SNP(CHR_NO, 0, Genotype(NONE, NONE));

static char nucleotide_char(const Nucleotide& n)
{
  switch ( n ) {
    case A:    return 'A';
    case C:    return 'C';
    case D:    return 'D';
    case G:    return 'G';
    case I:    return 'I';
    case NONE: return '-';
    case T:    return 'T';
  }
  return '-';
}

Nucleotide complement(const Nucleotide& n)
{
  switch ( n ) {
    case A:    return T;
    case C:    return G;
    case D:    return D;
    case G:    return C;
    case I:    return I;
    case NONE: return NONE;
    case T:    return A;
  }
  return NONE;
}

Genotype::Genotype() : first(NONE), second(NONE)
{
}

Genotype::Genotype(const Nucleotide& a, const Nucleotide& b)
  : first(a), second(b)
{
}

Genotype operator~(const Genotype& g)
{
  return Genotype(complement(g.first),
                  complement(g.second));
}

Genotype complement(const Genotype& g)
{
  return ~g;
}

bool Genotype::operator==(const Genotype& g) const
{
  return first == g.first && second == g.second;
}

bool Genotype::operator<(const Genotype& g) const
{
  if ( first < g.first )
    return true;

  if ( first > g.first )
    return false;

  return second < g.second;
}

std::string Genotype::to_string() const
{
  char s[3] = {0};

  s[0] = nucleotide_char(first);
  s[1] = nucleotide_char(second);

  if ( s[0] != '-' && s[1] == '-' )
    s[1] = '\0';

  return std::string(s);
}

SNP::SNP() :
  chromosome(CHR_NO),
  position(0),
  genotype(NONE, NONE)
{
}

SNP::SNP(const Chromosome& chr, const Position& pos, const Genotype& gt) :
  chromosome(chr),
  position(pos),
  genotype(gt)
{
}

SNP::SNP(const SNP& snp) :
  chromosome(snp.chromosome),
  position(snp.position),
  genotype(snp.genotype)
{
}

SNP& SNP::operator=(const SNP& snp) {
  if ( this != &snp ) {
    genotype = snp.genotype;
    chromosome = snp.chromosome;
    position = snp.position;
  }
  return *this;
}

bool SNP::operator==(const SNP& snp) const
{
  return position == snp.position &&
         chromosome == snp.chromosome &&
         genotype == snp.genotype;
}

bool SNP::operator<(const SNP& snp) const
{
  if ( position > snp.position )
    return false;
  if ( position < snp.position )
    return true;

  // equal position
  if ( chromosome > snp.chromosome )
    return false;
  if ( chromosome < snp.chromosome )
    return true;

  // equal chromosome
  return genotype < snp.genotype;
}

bool SNP::operator>(const SNP& snp) const
{
  return !(*this <= snp);
}

bool SNP::operator<=(const SNP& snp) const
{
  return *this == snp || *this < snp;
}

bool SNP::operator>=(const SNP& snp) const
{
  return *this == snp || *this > snp;
}

bool SNP::operator!=(const SNP& snp) const
{
  return !(*this == snp);
}

bool SNP::operator==(const Genotype& g) const
{
  return genotype == g;
}

struct GenomeIteratorImpl {
  SNPMap::const_iterator it;

  GenomeIteratorImpl(SNPMap::const_iterator& i):
    it(i)
  {
  }
};

GenomeIterator::GenomeIterator():
  pimpl(NULL)
{
}

GenomeIterator::GenomeIterator(GenomeIteratorImpl* p):
  pimpl(p)
{
}

GenomeIterator::~GenomeIterator()
{
  delete pimpl;
}

GenomeIterator::GenomeIterator(const GenomeIterator& o):
  pimpl(new GenomeIteratorImpl(o.pimpl->it))
{
}

GenomeIterator& GenomeIterator::operator=(const GenomeIterator& o)
{
  if ( pimpl != o.pimpl ) {
    delete pimpl;
    pimpl = new GenomeIteratorImpl(o.pimpl->it);
  }
  return *this;
}

void GenomeIterator::next()
{
  ++pimpl->it;
}

RsidSNP GenomeIterator::value() const
{
  return *pimpl->it;
}

bool GenomeIterator::operator==(const GenomeIterator& o) const
{
  return pimpl->it == o.pimpl->it;
}

bool GenomeIterator::operator!=(const GenomeIterator& o) const
{
  return pimpl->it != o.pimpl->it;
}

struct Genome::GenomeImpl {
  SNPMap snps;

  GenomeImpl(const std::size_t size) :
    snps(size)
  {
    snps.set_empty_key(0);
  }

  GenomeImpl(const GenomeImpl& g) :
    snps(g.snps)
  {
    snps.set_empty_key(0);
  }

  GenomeImpl& operator=(const GenomeImpl& g)
  {
    if ( this != &g )
      snps = g.snps;

    return *this;
  }

  bool contains(const RSID& rsid) const {
    return snps.find(rsid) != snps.end();
  }

  const SNP& operator[](const RSID& rsid) const {
    return !contains(rsid)? NONE_SNP : const_cast<SNPMap&>(snps)[rsid];
  }

  std::string genotype(const RSID& id) const {
    const SNP& snp = operator[](id);
    return snp.genotype.to_string();
  }
};

Genome::Genome():
  y_chromosome(false),
  pimpl(new GenomeImpl(0))
{
}

Genome::Genome(const std::size_t size):
  y_chromosome(false),
  pimpl(new GenomeImpl(size))
{
}

Genome::Genome(const Genome& g) :
  y_chromosome(g.y_chromosome),
  pimpl(new GenomeImpl(*g.pimpl))
{
}

Genome& Genome::operator=(const Genome& g)
{
  if ( this != &g ) {
    *pimpl = *g.pimpl;
    y_chromosome = g.y_chromosome;
  }
  return *this;
}

Genome::~Genome()
{
  delete pimpl;
}

const SNP& Genome::operator[](const RSID& rsid) const
{
  return (*pimpl)[rsid];
}

bool Genome::has(const RSID& rsid) const
{
  return pimpl->contains(rsid);
}

std::size_t Genome::size() const
{
  return pimpl->snps.size();
}

double Genome::load_factor() const
{
  return pimpl->snps.load_factor();
}

void Genome::insert(const RsidSNP& obj)
{
  pimpl->snps.insert(obj);
}

bool Genome::operator==(const Genome& o) const
{
  // cheap tests first
  if ( !(y_chromosome == o.y_chromosome && size() == o.size() ) )
    return false;
  else
    return o.pimpl->snps == pimpl->snps;
}

bool Genome::operator!=(const Genome& o) const
{
  return !(*this == o);
}

GenomeIterator Genome::begin() const
{
  auto i = const_cast<const SNPMap&>(pimpl->snps).begin();
  auto p = new GenomeIteratorImpl(i);
  return GenomeIterator(p);
}

GenomeIterator Genome::end() const
{
  auto i = const_cast<const SNPMap&>(pimpl->snps).end();
  auto p = new GenomeIteratorImpl(i);
  return GenomeIterator(p);
}

} // namespace arv
