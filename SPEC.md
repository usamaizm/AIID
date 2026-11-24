# AIID Draft Specification 0.1

**Status:** Draft for discussion. This is a proposed initial design, not a ratified standard.

## 1. Scope

AIID defines a portable descriptor document that identifies and describes a resource. A resource may be a file, program, AI agent, model, dataset, collection, service, device, or another digital or physical thing that can be referenced.

An AIID descriptor is metadata. It is not an executable, a replacement for the resource, or a container for the resource's primary payload.

## 2. Filename and companion relationship

Form a companion descriptor filename by appending .aiid to the complete resource filename:

- photo.jpeg becomes photo.jpeg.aiid
- archive.tar.gz becomes archive.tar.gz.aiid
- model.bin becomes model.bin.aiid

This preserves the original filename and makes the relationship discoverable by directory scanning. A descriptor may also refer to a resource by URI when no local companion file is available.

A collection-level descriptor may describe multiple resources, but its naming and discovery rules are not fixed in draft 0.1. Implementations must not assume every directory has one.

## 3. Encoding and serialization

### 3.1 Draft 0.1 baseline

Draft 0.1 uses UTF-8 encoded JSON as its required representation. JSON is a serialization choice, not the definition of the underlying AIID information model.

Readers must reject invalid UTF-8 and malformed JSON with a clear diagnostic. Writers should emit UTF-8 without a byte-order mark. Unknown fields should be ignored when not understood and preserved when practical.

### 3.2 Future encodings

The conceptual model is intended to be serialization-independent. A future revision may define a binary representation such as CBOR, provided it defines an unambiguous encoding identifier, equivalent field semantics, and interoperability tests. No binary encoding is standardized by draft 0.1.

Markdown is useful for documentation but is not the normative machine-readable representation in draft 0.1. A non-JSON representation must not silently be interpreted as JSON.

## 4. Core document structure

| Field | Requirement | Meaning |
|---|---|---|
| aiid_version | Required | Descriptor model version, currently 0.1 |
| identity | Required | Identifier and broad type of the described resource |
| resource | Optional | Reference and technical facts about the resource |
| description | Optional | Human-readable summary |
| metadata | Optional | Extensible descriptive metadata |
| provenance | Optional | Claims about origin, publisher, or creation |
| integrity | Optional | Content digest or other integrity information |
| links | Optional | Related resources or documentation |

Unknown properties should be tolerated for forward compatibility. Producers should not redefine existing field meanings.

## 5. Identity

identity.id is the identifier assigned to the described entity. It should be unique within its declared identifier scheme and stable for the lifetime of that entity. It is not a filesystem path and should not change merely because a file moves.

identity.type is a short type label such as image, document, application, dataset, model, agent, service, device, collection, or aidb-container. These examples are not a closed enumeration. Unknown type labels must be accepted.

The identity of an entity and the identity of a particular version or byte-level instance are different concepts. Draft 0.1 permits optional identity.version and integrity information, but does not mandate a universal version-ID or content-addressing scheme. A later revision should define those rules before claiming globally interoperable persistent identity.

## 6. Resource reference

resource.name may identify the expected companion filename. resource.uri may identify a resource by URI. resource.media_type may declare a media type where applicable.

Relative paths are interpreted relative to the descriptor's location. Implementations must prevent path traversal when resolving untrusted descriptors. A descriptor is data, not an instruction to execute, download, or open a resource automatically.

## 7. Extensibility and spatial data

AIID must not assume every resource is a conventional file or that all metadata is non-spatial. Spatial resources may be described through type labels, references, coordinate-system identifiers, units, bounds, or namespaced extension metadata where relevant.

Draft 0.1 does not define a geometry encoding, coordinate reference system registry, or spatial payload format. Large geometry, point clouds, maps, and other spatial payloads should remain in their native resource or an appropriate container such as AIDB. AIID can identify and describe those resources without duplicating their payload or imposing a competing spatial model.

Extensions should document units, coordinate reference systems, and semantics. Consumers must not guess units or coordinate systems.

## 8. Discovery

An implementation may discover a companion descriptor by appending .aiid to the complete resource filename. It may also discover descriptors through package indexes, registries, application metadata, or explicit references.

Discovery is optional. Failure to find a descriptor does not mean a resource is invalid or unidentified by other means. Implementations should not scan outside user-authorized locations.

## 9. Trust, safety, and permissions

An AIID descriptor is untrusted metadata unless independently verified. Statements about publisher, origin, safety, capabilities, permissions, or integrity are claims, not proof.

Cryptographic signatures, trusted publisher records, hashes, and authorization policies are separate mechanisms. Draft 0.1 reserves optional provenance and integrity sections but does not define a signature or permission protocol.

Consumers must not execute programs, grant permissions, follow external links, or disclose data solely because an AIID descriptor requests it.

## 10. Relationship to AIDB

AIDB is a container format; AIID is a descriptor and identification format. An AIID descriptor may describe an AIDB container, identify its version, and reference its contents or documentation. AIID does not define AIDB internals, and AIDB does not require AIID to function.

## 11. Conformance goals

A conforming 0.1 reader should:
1. Recognize the .aiid companion suffix.
2. Parse valid UTF-8 JSON.
3. Require aiid_version and identity.
4. Tolerate unknown fields and unknown resource type labels.
5. Treat descriptor content as untrusted data.
6. Avoid assuming the described resource is present or safe.

A conforming writer should produce valid UTF-8 JSON, include required fields, and avoid inventing verification claims.

## 12. Open issues for later drafts

- A formal globally unique identifier namespace and allocation procedure.
- Persistent entity identity versus version and content-instance identifiers.
- Collection descriptor naming and directory discovery precedence.
- A standardized binary serialization, if there is demonstrated need.
- Signature, publisher verification, and trust frameworks.
- Namespaced extension governance and spatial metadata conventions.
- A formal media type and schema publication location.
- Reference test vectors and an interoperability suite.
