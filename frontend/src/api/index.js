import WriterApi from "@/api/writer";
import FindingDependenciesApi from "@/api/finding_dependencies";
import MainApi from "@/api/main";

export default {
    writer: WriterApi,
    fd: FindingDependenciesApi,
    main: MainApi,
}